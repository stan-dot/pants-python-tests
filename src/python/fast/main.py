from fastapi import FastAPI

from mylib.main import hello

app = FastAPI()


@app.get("/")
async def root():
    # Return own string plus result of hello()
    own_string = "This is my own string."
    hello_result = hello()
    return {"message": f"{own_string} {hello_result}"}


# To run with uvicorn: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
