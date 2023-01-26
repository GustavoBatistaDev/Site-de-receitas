from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .test_base import RecipeBaseFunctionalTest 


class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):

    def test_recipe_home_page_not_found_recipes_text(self):
        self.browser.get(self.live_server_url)
        self.sleep(seconds=5)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('There are no recipes here!', body.text)

    def test_recipe_search_is_correct(self):
        recipes = self.make_recipe_in_batch()

        # Usuário abre a página
        self.browser.get(self.live_server_url)

        # ver um campo de busca com placeholder "Search recipes here..."
        search_input = self.browser.find_element(By.XPATH, '/html/body/div/div/form/input')  # noqa
        self.sleep(1)

        # clica na input e digita o termo de busca 
        # para que ache a receita com o titulo desejado
        search_input.send_keys(recipes[0].title)
        search_input.send_keys(Keys.ENTER)
        self.sleep(3)
        self.assertIn(
            'Recipe Title0.', self.browser.find_element(By.CLASS_NAME, 'main-content-list').text   # noqa
            ) 

       
