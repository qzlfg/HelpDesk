from fastapi import FastAPI


# Здесь будут импорты твоих роутеров, когда мы их напишем
# from app.api.routers import user_router, ticket_router


def create_app() -> FastAPI:
    """
    Фабрика по сборке FastAPI приложения.
    """
    app = FastAPI(
        title="HelpDesk API",
        description="Внутреннее API для системы управления заявками",
        version="0.0.1"
    )

    # 1. Настройка CORS (чтобы фронтенд мог делать запросы)
    # from fastapi.middleware.cors import CORSMiddleware
    # app.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=["*"], 
    #     allow_credentials=True,
    #     allow_methods=["*"],
    #     allow_headers=["*"],
    # )

    # 2. Подключение всех роутеров
    # app.include_router(user_router.router, prefix="/api/v1/users", tags=["Пользователи"])
    # app.include_router(ticket_router.router, prefix="/api/v1/tickets", tags=["Тикеты"])

    # 3. Здесь же можно добавить обработчики ошибок (Exception Handlers)
    
    return app

if __name__ == "__main__":
    # Глобальный экземпляр для Uvicorn.
    # При запуске команды `uvicorn main:app` сервер возьмет именно эту переменную.
    app = create_app()