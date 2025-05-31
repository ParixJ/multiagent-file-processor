
def decorator_main(func):
    async def wrapper(file):
        print('Routing agents...')
        result = await func(file)
        print('Done routing...')
        return result
    return wrapper

def decorator_intent(func):
    async def wrapper(*args,**kwargs):
        print('Getting file intent...')
        result = await func(*args,**kwargs)
        print('Intent classification completed.')
        return result 
    return wrapper

def decorator_urgency(func):
    async def wrapper(*args,**kwargs):
        print('Getting file urgency level...')
        result = await func(*args,**kwargs)
        print('Urgency classification completed.')
        return result 
    return wrapper
