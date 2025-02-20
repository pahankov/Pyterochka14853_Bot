# tests/test_recipes.py
async def test_recipes_handler():
    callback = AsyncMock(data="recipes")
    await handle_recipes(callback)
    callback.message.answer.assert_called_with("Рецепты недели: ...")