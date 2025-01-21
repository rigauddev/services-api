from app import create_app
from flask_asgi import WsgiToAsgi

app = create_app()

asgi_app = WsgiToAsgi(app)  # Adapta para ASGI

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(asgi_app, host='0.0.0.0', port=8000, reload=True)
