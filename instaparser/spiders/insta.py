import scrapy
from scrapy.http import HtmlResponse
from instaparser.items import InstaparserItem
import re
import json
from urllib.parse import urlencode
from copy import deepcopy


class InstaSpider(scrapy.Spider):
    name = 'insta'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = '***'
    inst_pwd = '***'
    parse_users = ['teliachi_nejnosti', 'autosto111']
    inst_graphql_link = 'https://www.instagram.com/graphql/query/?'
    posts_hash = '69cba40317214236af40e7efa697781d'
    friends_link = 'https://i.instagram.com/api/v1/friendships/show_many/'

    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.login,
            formdata={'username': self.inst_login, 'enc_password': self.inst_pwd},
            headers={'x-csrftoken': csrf}
        )

    def login(self, response: HtmlResponse):
        j_body = response.json()
        if j_body.get('authenticated'):
            for user in self.parse_users:
                yield response.follow(
                    f'/{user}',
                    callback=self.user_data_parse,
                    cb_kwargs={'username': user}
            )

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'count': 12}
        followings_data = f'{self.friends_link}/{user_id}/followings/?{urlencode(variables)}&search_surface=follow_list_page'
        yield response.follow(followings_data,
                              callback=self.followings_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'variables': deepcopy(variables)},
                              headers={'User-Agent': 'Instagram 155.0.0.37.107'})
        followers_data = f'{self.friends_link}/{user_id}/followers/?{urlencode(variables)}&search_surface=follow_list_page'
        yield response.follow(followers_data,
                              callback=self.followers_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'variables': deepcopy(variables)},
                              headers={'User-Agent': 'Instagram 155.0.0.37.107'})

    def followings_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        if j_data.get('next_max_id'):
            variables['max_id'] = j_data.get('next_max_id')
            followings_data = f'{self.friends_link}/{user_id}/followings/?{urlencode(variables)}&search_surface=follow_list_page'
            yield response.follow(followings_data,
                                  callback=self.followings_parse,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'variables': deepcopy(variables)},
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'})
        followings = j_data.get('users')
        for following in followings:
            item = InstaparserItem(username=following.get('username'),
                                   user_id=following.get('pk'),
                                   photo=following.get('profile_pic_url'))
            yield item

    def followers_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        if j_data.get('next_max_id'):
            variables['max_id'] = j_data.get('next_max_id')
            followers_data = f'{self.friends_link}/{user_id}/followers/?{urlencode(variables)}&search_surface=follow_list_page'
            yield response.follow(followers_data,
                                  callback=self.followers_parse,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'variables': deepcopy(variables)},
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'})
        followers = j_data.get('users')
        for follower in followers:
            item = InstaparserItem(username=follower.get('username'),
                                   user_id=follower.get('pk'),
                                   photo=follower.get('profile_pic_url'))
            yield item



    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        try:
            matched = re.search(
                '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
            ).group()
            return json.loads(matched).get('id')
        except:
            return re.findall('\"id\":\"\\d+\"', text)[-1].split('"')[-2]
