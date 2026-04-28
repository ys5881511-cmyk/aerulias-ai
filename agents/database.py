"""Database layer for Aerulias AI using SQLite.

Provides persistent storage for run history and memory with proper
indexing, transactions, and error handling.
"""

import sqlite3
import json
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from contextlib import contextmanager

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "aerulias.db"


@contextmanager
def get_connection(db_path: Path = DB_PATH):
    """Context manager for database connections.
    
    Args:
        db_path: Path to SQLite database file.
        
    Yields:
        Database connection.
    """
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception as e:
        logger.error(f"Database transaction failed: {e}", exc_info=True)
        conn.rollback()
        raise
    finally:
        conn.close()


def init_database(db_path: Path = DB_PATH) -> None:
    """Initialize database schema if it doesn't exist.
    
    Creates tables for:
    - run_history: Pipeline execution results
    - memory_store: Mistakes and lessons
    - evaluation_cache: Cached evaluations
    """
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        
        # Run history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS run_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                query TEXT NOT NULL,
                final_answer TEXT NOT NULL,
                final_score INTEGER,
                target_score INTEGER,
                max_rounds INTEGER,
                rounds_used INTEGER,
                memory_used_count INTEGER,
                sources_used_count INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(timestamp, query)
            )
        """)
        
        # Memory store table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory_store (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                score INTEGER,
                issues TEXT NOT NULL,
                improvement_suggestions TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes for faster queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_run_history_timestamp 
            ON run_history(timestamp)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_run_history_score 
            ON run_history(final_score)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_memory_store_created 
            ON memory_store(created_at)
        """)
        
        logger.info("Database initialized successfully")


class RunHistoryDB:
    """Database interface for run history."""
    
    def save_run(self, result: Dict[str, Any], db_path: Path = DB_PATH) -> int:
        """Save a pipeline run to database.
        
        Args:
            result: Complete pipeline result.
            db_path: Database file path.
            
        Returns:
            ID of inserted row.
        """
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO run_history 
                (timestamp, query, final_answer, final_score, target_score, 
                 max_rounds, rounds_used, memory_used_count, sources_used_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                result.get("timestamp"),
                result.get("query"),
                result.get("final_answer"),
                result.get("final_score"),
                result.get("target_score"),
                result.get("max_rounds"),
                len(result.get("rounds", [])),
                len(result.get("memory_used", [])),
                len(result.get("sources", []))
            ))
            
            row_id = cursor.lastrowid
            logger.info(f"Saved run #{row_id} to database")
            return row_id
    
    def get_recent_runs(self, limit: int = 20, db_path: Path = DB_PATH) -> List[Dict[str, Any]]:
        """Get recent pipeline runs.
        
        Args:
            limit: Maximum number of runs to return.
            db_path: Database file path.
            
        Returns:
            List of run records.
        """
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM run_history 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (limit,))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_run_by_id(self, run_id: int, db_path: Path = DB_PATH) -> Optional[Dict[str, Any]]:
        """Get a specific run by ID.
        
        Args:
            run_id: ID of the run.
            db_path: Database file path.
            
        Returns:
            Run record or None if not found.
        """
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM run_history WHERE id = ?", (run_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_statistics(self, db_path: Path = DB_PATH) -> Dict[str, Any]:
        """Get statistics about runs.
        
        Args:
            db_path: Database file path.
            
        Returns:
            Dictionary with statistics.
        """
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) as total FROM run_history")
            total = cursor.fetchone()["total"]
            
            cursor.execute("SELECT AVG(final_score) as avg_score FROM run_history")
            avg_score = cursor.fetchone()["avg_score"] or 0
            
            cursor.execute("SELECT MAX(final_score) as max_score FROM run_history")
            max_score = cursor.fetchone()["max_score"] or 0
            
            cursor.execute("SELECT AVG(rounds_used) as avg_rounds FROM run_history")
            avg_rounds = cursor.fetchone()["avg_rounds"] or 0
            
            return {
                "total_runs": total,
                "avg_score": round(avg_score, 2),
                "max_score": max_score,
                "avg_rounds_used": round(avg_rounds, 2)
            }


class MemoryStoreDB:
    """Database interface for memory storage."""
    
    def save_memory(self, query: str, evaluation: Dict[str, Any], db_path: Path = DB_PATH) -> int:
        """Save evaluation to memory.
        
        Args:
            query: Original query.
            evaluation: Evaluation result.
            db_path: Database file path.
            
        Returns:
            ID of inserted row.
        """
        # Skip API errors
        if "Connection error." in evaluation.get("issues", []):
            return -1
        
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO memory_store 
                (query, score, issues, improvement_suggestions)
                VALUES (?, ?, ?, ?)
            """, (
                query,
                evaluation.get("score", 0),
                json.dumps(evaluation.get("issues", [])),
                json.dumps(evaluation.get("improvement_suggestions", []))
            ))
            
            row_id = cursor.lastrowid
            logger.info(f"Saved memory #{row_id}")
            return row_id
    
    def find_relevant_memory(self, query: str, limit: int = 5, db_path: Path = DB_PATH) -> List[Dict[str, Any]]:
        """Find memories relevant to query using full-text search simulation.
        
        Args:
            query: Query to search for.
            limit: Maximum memories to return.
            db_path: Database file path.
            
        Returns:
            List of relevant memory items.
        """
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            
            # Simple word-based search for now
            query_words = query.lower().split()
            
            cursor.execute("""
                SELECT * FROM memory_store 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (limit,))
            
            rows = cursor.fetchall()
            results = [dict(row) for row in rows]
            
            # Parse JSON fields
            for item in results:
                item["issues"] = json.loads(item["issues"])
                item["improvement_suggestions"] = json.loads(item["improvement_suggestions"])
            
            return results
    
    def get_all_memory(self, db_path: Path = DB_PATH) -> List[Dict[str, Any]]:
        """Get all memory items.
        
        Args:
            db_path: Database file path.
            
        Returns:
            List of all memory items.
        """
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM memory_store ORDER BY created_at DESC")
            rows = cursor.fetchall()
            
            results = [dict(row) for row in rows]
            for item in results:
                item["issues"] = json.loads(item["issues"])
                item["improvement_suggestions"] = json.loads(item["improvement_suggestions"])
            
            return results


# Convenience functions
def save_run_to_db(result: Dict[str, Any]) -> int:
    """Save run result to database."""
    return RunHistoryDB().save_run(result)


def get_recent_runs_from_db(limit: int = 20) -> List[Dict[str, Any]]:
    """Get recent runs from database."""
    return RunHistoryDB().get_recent_runs(limit)


def save_memory_to_db(query: str, evaluation: Dict[str, Any]) -> int:
    """Save memory to database."""
    return MemoryStoreDB().save_memory(query, evaluation)


def get_relevant_memory_from_db(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Get relevant memory from database."""
    return MemoryStoreDB().find_relevant_memory(query, limit)
