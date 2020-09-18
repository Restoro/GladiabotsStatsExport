# -*- coding: utf-8 -*-
import scrapy


class GladiaspiderSpider(scrapy.Spider):
    name = 'gladiaspider'

    def start_requests(self):
        self.current_results = 0
        self.current_page = 1
        self.max_results = int(getattr(self, 'max_r', 100))
        self.player = getattr(self, 'player', 'ThordanSsoa')
        urls = [
            'https://stats.gladiabots.com/player?&display=matches&matchMode=1&name={}&page=1'.format(self.player)
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        table = response.css("#matchesTable")

        if not table.css('tr').css('td'):
            return

        for matchresult in table.css('tr'):
            if not matchresult.css('td'):
                continue
            else:
                if self.current_results < self.max_results:
                    self.current_results+=1

                yield {
                    'matchid': matchresult.css('td::text')[1].get(),
                    'current_elo': matchresult.css('td[class="leftPlayer"] span::text').get().split()[0].replace('(',''),
                    'enemy_elo':   matchresult.css('td[class="rightPlayer"] span::text').get().split()[0].replace('(',''),
                    'enemy_name':  matchresult.css('td[class="rightPlayer"] .player::text').get(),
                    'gained points': matchresult.css('td[class="leftPlayer"] span::text').get().split()[1].replace(')',''),
                    'outcome': self.get_outcome(matchresult)
                }

        if self.current_results < self.max_results:
            self.current_page += 1
            next_page = 'https://stats.gladiabots.com/player?&display=matches&matchMode=1&name={0}&page={1}'.format(self.player, self.current_page)
            print(next_page)
            if next_page is not None:
                yield response.follow(next_page, self.parse)

    def get_outcome(self, matchresult):
        outcome_text = 'draw'
        outcome = matchresult.css('.leftPlayer.victory')
        if not outcome:
            outcome = matchresult.css('.draw')
            if not outcome:
                outcome_text = 'defeat'
        else:
            outcome_text = 'victory'
        return outcome_text

