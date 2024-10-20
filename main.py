from fastapi import FastAPI, Body
from lunisolar import ChineseDate
from pydantic import BaseModel, Field, validator

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Define a Pydantic model for the request body
class DateInput(BaseModel):
    year: str = Field(..., min_length=3, max_length=4)
    month: str = Field(..., min_length=2, max_length=2)
    day: str = Field(..., min_length=2, max_length=2)

    @validator('year', 'month', 'day')
    def validate_numeric(cls, v):
        if not v.isdigit():
            raise ValueError('Must contain only digits')
        return v

    def to_int(self):
        return {
            'year': int(self.year),
            'month': int(self.month),
            'day': int(self.day)
        }

@app.post('/getZodiac')
async def getZodiacPost(date_input: DateInput):
    date_dict = date_input.to_int()
    entered_date = ChineseDate.from_gregorian(
        date_dict['year'], date_dict['month'], date_dict['day'])
    return {"result": entered_date.zodiac}
