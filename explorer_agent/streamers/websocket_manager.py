"""
WebSocket manager for real-time job streaming

Manages WebSocket connections and broadcasts job data to connected clients
"""

import asyncio
import json
import logging
from typing import Dict, List, Set, Any
from fastapi import WebSocket

logger = logging.getLogger(__name__)

class WebSocketManager:
    """Manages WebSocket connections for real-time streaming"""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.connection_metadata: Dict[WebSocket, Dict[str, Any]] = {}
        
    async def connect(self, websocket: WebSocket):
        """Accept a new WebSocket connection"""
        await websocket.accept()
        self.active_connections.add(websocket)
        
        # Store connection metadata
        self.connection_metadata[websocket] = {
            "connected_at": asyncio.get_event_loop().time(),
            "last_activity": asyncio.get_event_loop().time(),
            "messages_sent": 0,
            "messages_received": 0
        }
        
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")
        
        # Send welcome message
        await self.send_personal_message({
            "type": "connection_status",
            "message": "Connected to Explorer Agent",
            "connection_id": id(websocket)
        }, websocket)
        
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection"""
        self.active_connections.discard(websocket)
        
        # Clean up metadata
        if websocket in self.connection_metadata:
            del self.connection_metadata[websocket]
            
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")
        
    async def send_personal_message(self, message: Any, websocket: WebSocket):
        """Send a message to a specific WebSocket connection"""
        try:
            if isinstance(message, dict):
                message_json = json.dumps(message)
            else:
                message_json = json.dumps({"message": str(message)})
                
            await websocket.send_text(message_json)
            
            # Update metadata
            if websocket in self.connection_metadata:
                self.connection_metadata[websocket]["messages_sent"] += 1
                self.connection_metadata[websocket]["last_activity"] = asyncio.get_event_loop().time()
                
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
            await self.disconnect(websocket)
            
    async def broadcast(self, message: Any):
        """Broadcast a message to all connected WebSocket clients"""
        if not self.active_connections:
            return
            
        # Convert message to JSON if it's a dict
        if isinstance(message, dict):
            message_json = json.dumps(message)
        else:
            message_json = json.dumps({"message": str(message)})
            
        # Send to all connections
        disconnected = set()
        for websocket in self.active_connections:
            try:
                await websocket.send_text(message_json)
                
                # Update metadata
                if websocket in self.connection_metadata:
                    self.connection_metadata[websocket]["messages_sent"] += 1
                    self.connection_metadata[websocket]["last_activity"] = asyncio.get_event_loop().time()
                    
            except Exception as e:
                logger.error(f"Error broadcasting to WebSocket: {e}")
                disconnected.add(websocket)
                
        # Remove disconnected connections
        for websocket in disconnected:
            self.disconnect(websocket)
            
        logger.info(f"Broadcasted message to {len(self.active_connections)} connections")
        
    async def broadcast_job_data(self, job_data: Dict[str, Any], scraper_name: str = ""):
        """Broadcast job data to all connected clients"""
        message = {
            "type": "job_data",
            "scraper": scraper_name,
            "timestamp": asyncio.get_event_loop().time(),
            "data": job_data
        }
        
        await self.broadcast(message)
        
    async def broadcast_status_update(self, status: str, message: str = "", data: Dict[str, Any] = None):
        """Broadcast status updates to all connected clients"""
        update_message = {
            "type": "status_update",
            "status": status,
            "message": message,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        if data:
            update_message["data"] = data
            
        await self.broadcast(update_message)
        
    async def broadcast_scraper_status(self, scraper_name: str, status: str, message: str = ""):
        """Broadcast scraper status updates"""
        status_message = {
            "type": "scraper_status",
            "scraper": scraper_name,
            "status": status,
            "message": message,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        await self.broadcast(status_message)
        
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get statistics about current connections"""
        total_connections = len(self.active_connections)
        total_messages_sent = sum(
            meta["messages_sent"] for meta in self.connection_metadata.values()
        )
        total_messages_received = sum(
            meta["messages_received"] for meta in self.connection_metadata.values()
        )
        
        return {
            "total_connections": total_connections,
            "total_messages_sent": total_messages_sent,
            "total_messages_received": total_messages_received,
            "connection_details": [
                {
                    "connection_id": id(conn),
                    "connected_at": meta["connected_at"],
                    "last_activity": meta["last_activity"],
                    "messages_sent": meta["messages_sent"],
                    "messages_received": meta["messages_received"]
                }
                for conn, meta in self.connection_metadata.items()
            ]
        }
        
    async def ping_all_connections(self):
        """Send ping to all connections to check if they're still alive"""
        ping_message = {
            "type": "ping",
            "timestamp": asyncio.get_event_loop().time()
        }
        
        await self.broadcast(ping_message)
        
    async def cleanup_inactive_connections(self, max_inactive_time: float = 300):
        """Remove connections that have been inactive for too long"""
        current_time = asyncio.get_event_loop().time()
        inactive_connections = set()
        
        for websocket, metadata in self.connection_metadata.items():
            if current_time - metadata["last_activity"] > max_inactive_time:
                inactive_connections.add(websocket)
                
        for websocket in inactive_connections:
            logger.info(f"Removing inactive connection {id(websocket)}")
            await self.disconnect(websocket)
            
        if inactive_connections:
            logger.info(f"Cleaned up {len(inactive_connections)} inactive connections")

