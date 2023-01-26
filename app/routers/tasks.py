from fastapi import APIRouter, BackgroundTasks, Depends, status

from jwt import get_current_user

from back_tasks import tasks

router = APIRouter(tags=['mail'], prefix="/report")


@router.get("/dashboard", status_code=status.HTTP_200_OK)
def get_dashboard_report(background_tasks: BackgroundTasks, current_user=Depends(get_current_user)):
    background_tasks.add_task(tasks.send_email_report_dashboard, current_user)
    return {
        "status": status.HTTP_200_OK,
        "data": "Вам отправлено письмо",
    }
