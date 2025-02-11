from pydantic import BaseModel

class ProcessProtocolRequest(BaseModel):
    protocolId: str
    userId: str