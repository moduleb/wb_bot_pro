import uvicorn
from fastapi import FastAPI
from starlette.responses import RedirectResponse

from fastapi_app import views

# Создание приложения
app = FastAPI(title="WB_BOT_PRO")
app.include_router(views.router, tags=["Websocket"])

# Redirect на страницу документации при обращении на "/"
@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirect to /openapi.json when accessing "/" endpoint"""
    return RedirectResponse(url="/docs")

# Запуск
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', log_level="debug")