from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from csv import writer
from time import sleep
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS


driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))

driver.maximize_window()
driver.get('https://www.tripadvisor.com/Hotel_Review-g187849-d2340336-Reviews-Armani_Hotel-Milan_Lombardy.html')

cookies_wait = WebDriverWait(driver, 3)
cookies_accept = cookies_wait.until(lambda d: d.find_element('xpath', '//*[@id="onetrust-accept-btn-handler"]'))
cookies_accept.click()

with open('Armani hotel reviews.csv', 'w', encoding='UTF-8', newline='') as file:
	file.write('Score,Date,Title,Comment,Page\n')
	
	for page in range(1, 11):
		expand = driver.find_element('xpath', './/div[contains(@data-test-target, "expand-review")]')
		expand and expand.click()
		
		reviews = driver.find_elements('xpath', './/div[@data-reviewid]')
		for review in reviews:
			score = review.find_element('xpath', './/span[contains(@class, "ui_bubble_rating bubble_")]').get_attribute('class').split('_')[3]
			date = review.find_element('xpath', './/span[@class="teHYY _R Me S4 H3"]').text[14:]
			title = review.find_element('xpath', './/div[contains(@data-test-target, "review-title")]').text
			comment = review.find_element('xpath', './/span[@class="QewHA H4 _a"]').text.replace('\n', ' ')
			
			writer(file).writerow([score,date,title,comment,page])
		
		driver.find_element('xpath', './/a[@class="ui_button nav next primary "]').click()
		sleep(1)

driver.quit()


df = pd.read_csv('Armani hotel reviews.csv')

df['Year'] = pd.to_datetime(df['Date']).dt.year

sns.boxplot(x='Score', y='Year', data=df)
plt.title('Box Plot of Scores by Year')
plt.xlabel('Year')
plt.ylabel('Score')
plt.show()

sns.countplot(x='Score', data=df)
plt.title('Count Plot of Scores')
plt.xlabel('Score')
plt.ylabel('Count')
plt.show()


stopwords = set(STOPWORDS)
stopwords.update(['armani', 'hotel', 'room'])

reviews = ' '.join(df.Comment)
wordcloud = WordCloud(stopwords=stopwords).generate(reviews)

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()


df['sentiment'] = df['Score'].apply(lambda score: +1 if score > 30 else -1)

positive = df[df['sentiment'] == 1]
negative = df[df['sentiment'] == -1]

wordcloud_pos = WordCloud(stopwords=stopwords).generate(' '.join(word for word in positive.Title))
wordcloud_neg = WordCloud(stopwords=stopwords).generate(' '.join(word for word in negative.Title))

fig, axes = plt.subplots(1, 2, figsize=(17, 4.5))

axes[0].imshow(wordcloud_pos, interpolation='bilinear')
axes[0].axis('off')
axes[0].set_title('Positives')

axes[1].imshow(wordcloud_neg, interpolation='bilinear')
axes[1].axis('off')
axes[1].set_title('Negatives')

fig.suptitle('Hotel Armani')
fig.show()
