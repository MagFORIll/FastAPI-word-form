import shortuuid
from fastapi import UploadFile, File, APIRouter
from fastapi.responses import StreamingResponse
from app.services.services import create_excel_from_stats
from app.celery.celery_worker import process_file_task

router = APIRouter()


@router.post("/public/report/export/")
async def upload_file(file: UploadFile = File):
    """Загрузка файла пользователя для дальнейшей обработки"""
    public_id = shortuuid.uuid()[:8]
    json_path = f'app/API/endpoints/data_{public_id}.json'

    content = file.file.read().decode()

    task = process_file_task.delay(content, json_path)

    return {
        "task_id": task.id,
        "status_url": f"/public/report/export/status/{task.id}",
        "download_template": f"/public/report/export/{public_id}"
    }

@router.get("/public/report/export/")
async def download_file():
    """Выгрузка файла с результатами пользователю в формате xlsx"""
    try:
        excel_file = create_excel_from_stats()
        return StreamingResponse(
            excel_file,
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={'Content-Disposition': 'attachment; filename=result.xlsx'}
        )
    except FileNotFoundError:
        from fastapi import HTTPException
        raise HTTPException(404, "Сначала загрузите файл через POST")
