'use client';

import { useEffect, useState, useRef, useCallback } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { AlertCircle, CheckCircle2, Loader2 } from 'lucide-react';

export default function WebSocketComponent() {
  const [messages, setMessages] = useState<string[]>([]);
  const [status, setStatus] = useState<'connecting' | 'connected' | 'disconnected'>('disconnected');
  const wsRef = useRef<WebSocket | null>(null);

  const connect = useCallback(() => {
    // Đóng connection cũ nếu còn
    if (wsRef.current) {
      wsRef.current.close();
    }

    setStatus('connecting');
    console.log('Attempting to connect...');

    try {
      const ws = new WebSocket('ws://localhost:8000/api/v1/ws');
      wsRef.current = ws;

      ws.onopen = () => {
        console.log('WebSocket connected');
        setStatus('connected');
        setMessages(prev => [...prev, `[${new Date().toLocaleTimeString()}] ✅ Connected to server`]);
      };

      ws.onmessage = (event) => {
        console.log('Received:', event.data);
        try {
          const data = JSON.parse(event.data);
          const time = new Date(data.timestamp).toLocaleTimeString();
          setMessages(prev => [...prev.slice(-9), `[${time}] ${data.message}`]);
        } catch (error) {
          console.error('Failed to parse message:', error);
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        setStatus('disconnected');
        setMessages(prev => [...prev, `[${new Date().toLocaleTimeString()}] ❌ Connection error`]);
      };

      ws.onclose = () => {
        console.log('WebSocket disconnected');
        setStatus('disconnected');
        setMessages(prev => [...prev, `[${new Date().toLocaleTimeString()}] 🔌 Disconnected from server`]);
      };
    } catch (error) {
      console.error('Failed to create WebSocket:', error);
      setStatus('disconnected');
      setMessages(prev => [...prev, `[${new Date().toLocaleTimeString()}] ❌ Failed to connect`]);
    }
  }, []);

  useEffect(() => {
    // Tự động connect khi component mount
    connect();

    // Cleanup khi unmount
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [connect]);

  const getStatusIcon = () => {
    switch (status) {
      case 'connected':
        return <CheckCircle2 className="w-4 h-4 text-green-600" />;
      case 'connecting':
        return <Loader2 className="w-4 h-4 text-yellow-600 animate-spin" />;
      case 'disconnected':
        return <AlertCircle className="w-4 h-4 text-red-600" />;
    }
  };

  const getStatusText = () => {
    switch (status) {
      case 'connected':
        return 'Connected';
      case 'connecting':
        return 'Connecting...';
      case 'disconnected':
        return 'Lost Connection';
    }
  };

  const getStatusColor = () => {
    switch (status) {
      case 'connected':
        return 'text-green-600';
      case 'connecting':
        return 'text-yellow-600';
      case 'disconnected':
        return 'text-red-600';
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>WebSocket Real-time Connection</CardTitle>
        <CardDescription className="flex items-center gap-2">
          {getStatusIcon()}
          <span className={`font-semibold ${getStatusColor()}`}>
            {getStatusText()}
          </span>
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {/* Hiển thị alert khi mất kết nối */}
          {status === 'disconnected' && (
            <div className="bg-red-50 border border-red-200 rounded-md p-4">
              <div className="flex items-center gap-2 mb-2">
                <AlertCircle className="w-5 h-5 text-red-600" />
                <h4 className="font-semibold text-red-800">Connection Lost</h4>
              </div>
              <p className="text-sm text-red-700 mb-3">
                Unable to connect to the WebSocket server. Please check if the backend is running.
              </p>
              <Button 
                onClick={connect}
                variant="destructive"
                size="sm"
              >
                Reconnect
              </Button>
            </div>
          )}

          {/* Hiển thị nút reconnect khi đang connected (optional) */}
          {status === 'connected' && (
            <div className="flex justify-between items-center">
              <p className="text-sm text-gray-600">Receiving messages every 5 seconds</p>
              <Button 
                onClick={connect}
                variant="outline"
                size="sm"
              >
                Reconnect
              </Button>
            </div>
          )}

          {/* Messages log */}
          <div className="space-y-2">
            <h3 className="font-semibold text-sm">Messages Log:</h3>
            <div className="bg-gray-100 dark:bg-gray-800 p-4 rounded-md max-h-64 overflow-y-auto">
              {messages.length === 0 ? (
                <p className="text-gray-500 text-sm">Waiting for messages...</p>
              ) : (
                <div className="space-y-1">
                  {messages.map((msg, idx) => (
                    <div key={idx} className="text-xs font-mono text-gray-700 dark:text-gray-300">
                      {msg}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}