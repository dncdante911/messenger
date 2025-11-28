from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any

# РЎС…РµРјР° РґР»СЏ РєРѕРјР°РЅРґС‹, РєРѕС‚РѕСЂСѓСЋ РєР»РёРµРЅС‚ РѕС‚РїСЂР°РІР»СЏРµС‚ РїРѕ WebSocket
class WSCommand(BaseModel):
    type: str = Field(..., description="РўРёРї РєРѕРјР°РЅРґС‹: SEND_MSG, TYPING, READ")
    payload: Any = Field(..., description="РџРѕР»РµР·РЅР°СЏ РЅР°РіСЂСѓР·РєР° РєРѕРјР°РЅРґС‹")

# РЎС…РµРјР° РґР»СЏ РїРѕР»РµР·РЅРѕР№ РЅР°РіСЂСѓР·РєРё РєРѕРјР°РЅРґС‹ SEND_MSG
class WSMessagePayload(BaseModel):
    recipient_id: int
    content: str # Р—Р°С€РёС„СЂРѕРІР°РЅРЅС‹Р№ РєРѕРЅС‚РµРЅС‚

# РЎС…РµРјР° РґР»СЏ РёСЃС…РѕРґСЏС‰РµРіРѕ СЃРѕРѕР±С‰РµРЅРёСЏ (СЃРµСЂРІРµСЂ -> РєР»РёРµРЅС‚)
class MessageOut(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    content: str
    created_at: datetime