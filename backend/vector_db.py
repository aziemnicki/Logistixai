"""
ChromaDB Vector Database Setup for local RAG and semantic search.
Free, local, persistent vector storage with automatic embeddings.
"""

import chromadb
from chromadb.config import Settings as ChromaSettings
from config import settings
import os
from typing import List, Dict, Any, Optional


class VectorDB:
    """ChromaDB client wrapper for vector storage and retrieval."""

    def __init__(self):
        """Initialize ChromaDB with persistent storage."""
        # Ensure data directory exists
        os.makedirs(settings.CHROMA_DB_PATH, exist_ok=True)

        # Initialize ChromaDB client with persistent storage
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_DB_PATH,
            settings=ChromaSettings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )

        # Create/get collections
        self.reports_collection = self.client.get_or_create_collection(
            name="reports",
            metadata={"description": "Compliance reports with embeddings for semantic search"}
        )

        self.search_results_collection = self.client.get_or_create_collection(
            name="search_results",
            metadata={"description": "Web search results for RAG context"}
        )

        self.pdfs_collection = self.client.get_or_create_collection(
            name="pdf_reports",
            metadata={"description": "PDF reports with metadata for retrieval"}
        )

    def add_report(
        self,
        report_id: str,
        report_content: str,
        metadata: Dict[str, Any]
    ) -> None:
        """
        Add a report to the vector database with automatic embeddings.

        Args:
            report_id: Unique report identifier
            report_content: Full report content as string
            metadata: Additional metadata (company_name, generated_at, etc.)
        """
        self.reports_collection.add(
            ids=[report_id],
            documents=[report_content],
            metadatas=[metadata]
        )

    def add_search_results(
        self,
        report_id: str,
        search_results: List[Dict[str, str]]
    ) -> None:
        """
        Add search results to vector database for RAG context.

        Args:
            report_id: Associated report ID
            search_results: List of search results with url, title, snippet
        """
        ids = []
        documents = []
        metadatas = []

        for idx, result in enumerate(search_results):
            result_id = f"{report_id}_search_{idx}"
            document = f"{result.get('title', '')} {result.get('snippet', '')}"

            ids.append(result_id)
            documents.append(document)
            metadatas.append({
                "report_id": report_id,
                "url": result.get("url", ""),
                "title": result.get("title", ""),
                "type": "search_result"
            })

        if ids:
            self.search_results_collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )

    def search_reports(
        self,
        query: str,
        n_results: int = 5,
        where: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Semantic search across all reports.

        Args:
            query: Search query
            n_results: Number of results to return
            where: Optional metadata filters

        Returns:
            Dictionary with documents, metadatas, distances
        """
        return self.reports_collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where
        )

    def get_report_context(
        self,
        report_id: str,
        query: str,
        n_results: int = 3
    ) -> List[str]:
        """
        Retrieve relevant context from a specific report for RAG.

        Args:
            report_id: Report to search within
            query: User question
            n_results: Number of context chunks to retrieve

        Returns:
            List of relevant text chunks
        """
        results = self.reports_collection.query(
            query_texts=[query],
            where={"report_id": report_id},
            n_results=n_results
        )

        return results.get("documents", [[]])[0]

    def get_search_results_context(
        self,
        report_id: str,
        query: str,
        n_results: int = 5
    ) -> List[Dict[str, str]]:
        """
        Retrieve relevant search results for RAG context.

        Args:
            report_id: Associated report ID
            query: User question
            n_results: Number of results to retrieve

        Returns:
            List of relevant search results with metadata
        """
        results = self.search_results_collection.query(
            query_texts=[query],
            where={"report_id": report_id},
            n_results=n_results
        )

        contexts = []
        if results.get("metadatas") and results.get("documents"):
            for metadata, doc in zip(results["metadatas"][0], results["documents"][0]):
                contexts.append({
                    "url": metadata.get("url", ""),
                    "title": metadata.get("title", ""),
                    "content": doc
                })

        return contexts

    def get_report_by_id(self, report_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific report from ChromaDB."""
        result = self.reports_collection.get(ids=[report_id])

        if result and result.get("ids"):
            return {
                "id": result["ids"][0],
                "content": result["documents"][0],
                "metadata": result["metadatas"][0]
            }
        return None

    def delete_report(self, report_id: str) -> None:
        """Delete a report and its associated search results."""
        # Delete report
        try:
            self.reports_collection.delete(ids=[report_id])
        except Exception:
            pass

        # Delete associated search results
        try:
            # Get all search results for this report
            results = self.search_results_collection.get(
                where={"report_id": report_id}
            )
            if results and results.get("ids"):
                self.search_results_collection.delete(ids=results["ids"])
        except Exception:
            pass

    def count_reports(self) -> int:
        """Get total number of reports in database."""
        return self.reports_collection.count()

    def add_pdf(
        self,
        report_id: str,
        pdf_base64: str,
        pdf_path: str,
        metadata: Dict[str, Any]
    ) -> None:
        """
        Store PDF report in vector database with metadata.

        Args:
            report_id: Report identifier
            pdf_base64: Base64 encoded PDF content
            pdf_path: File system path to PDF
            metadata: Additional metadata (company_name, generated_at, etc.)
        """
        # Store PDF metadata and small excerpt for embedding
        # We don't embed the full base64, just metadata
        metadata_text = f"""
        PDF Report for {metadata.get('company_name', 'Unknown')}
        Report ID: {report_id}
        Generated: {metadata.get('generated_at', 'Unknown')}
        Status: {metadata.get('status', 'unknown')}
        """

        full_metadata = {
            **metadata,
            "report_id": report_id,
            "pdf_path": pdf_path,
            "pdf_size_bytes": len(pdf_base64),
            "type": "pdf"
        }

        self.pdfs_collection.add(
            ids=[f"pdf_{report_id}"],
            documents=[metadata_text],  # Searchable text
            metadatas=[full_metadata]
        )

    def get_pdf_metadata(self, report_id: str) -> Optional[Dict[str, Any]]:
        """
        Get PDF metadata from vector database.

        Args:
            report_id: Report identifier

        Returns:
            PDF metadata dictionary or None
        """
        try:
            result = self.pdfs_collection.get(ids=[f"pdf_{report_id}"])

            if result and result.get("ids"):
                return result["metadatas"][0]
            return None
        except Exception as e:
            print(f"Error retrieving PDF metadata: {e}")
            return None

    def search_pdfs(
        self,
        query: str,
        n_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for PDF reports by semantic similarity.

        Args:
            query: Search query
            n_results: Maximum results

        Returns:
            List of matching PDF metadata
        """
        results = self.pdfs_collection.query(
            query_texts=[query],
            n_results=n_results
        )

        pdf_results = []
        if results.get("metadatas") and results["metadatas"][0]:
            for metadata in results["metadatas"][0]:
                pdf_results.append(metadata)

        return pdf_results

    def delete_pdf(self, report_id: str) -> None:
        """Delete PDF from vector database."""
        try:
            self.pdfs_collection.delete(ids=[f"pdf_{report_id}"])
        except Exception:
            pass

    def reset_database(self) -> None:
        """Reset all collections (use with caution!)."""
        self.client.delete_collection("reports")
        self.client.delete_collection("search_results")
        self.client.delete_collection("pdf_reports")

        # Recreate collections
        self.reports_collection = self.client.get_or_create_collection(
            name="reports",
            metadata={"description": "Compliance reports with embeddings for semantic search"}
        )
        self.search_results_collection = self.client.get_or_create_collection(
            name="search_results",
            metadata={"description": "Web search results for RAG context"}
        )
        self.pdfs_collection = self.client.get_or_create_collection(
            name="pdf_reports",
            metadata={"description": "PDF reports with metadata for retrieval"}
        )


# Global vector database instance
vector_db = VectorDB()


def init_vector_db() -> VectorDB:
    """Initialize and return vector database instance."""
    return vector_db
