import re
import jieba
import jieba.analyse
jieba.initialize()


from pymongo import MongoClient
from lxml import etree
client = MongoClient('192.168.1.202')
db = client['weibo-search']
collection = db.webpages


def jieba_cut(text):
    stop_words = '。，？：@—,、！![]【】《》“”.…#~°- '
    text = re.sub(r'(@.+?)[:\s]', r'', text, re.S)
    text = re.sub(r'(#.+?#)', r'', text, re.S)
    return list(filter(
        lambda x: x.strip(stop_words),
        # jieba.cut_for_search(text),
        jieba.analyse.extract_tags(text, topK=50, withWeight=False),
    ))


def etl_weibo_search(_id):
    doc = collection.find_one({'_id': _id})
    body = doc['collected']['body']
    keyword = doc['collected']['keyword'].strip('@')
    if keyword.lower() not in body.lower():
        return
    tree = etree.HTML(body)
    if not tree:
        return
    for status in tree.xpath(".//div[@action-type='feed_list_item']"):
        mid = status.xpath(".//@mid")[0]
        context = [
            ''.join(t.itertext())
            for t in status.xpath(".//p[@class='comment_txt']")]
        nick = status.xpath(".//p[@class='comment_txt']/@nick-name")[0]
        link = status.xpath(".//div[contains(@class,'feed_from')]/a/@href")[0]
        comments_count = status.xpath(
            ".//ul[contains(@class,'feed_action_info')]/li[3]//em/text()")
        comments_count = comments_count and int(comments_count[0]) or 0
        db.statuses.update({
            'mid': mid,
        }, {
            '$set': {
                'keyword': keyword,
                'mid': mid,
                'context': context,
                'nick': nick,
                'link': link,
                'commentsCount': comments_count,
                'link_id': re.search(r'weibo\.com/(.+)$', link).group(1),
                'jieba': sum([jieba_cut(t) for t in context], []),
            }
        }, upsert=True)

        if comments_count > 0:
            row = db.seeds.find_one({'mid': mid})
            if not row:
                db.seeds.insert({
                    'mid': mid,
                    'url': link,
                    'ok': False,
                    'status': 'enqueue',
                })


def etl_weibo_comments(_id):
    doc = collection.find_one({'_id': _id})
    body = doc['collected']['body']
    tree = etree.HTML(body)
    if not tree:
        print('body not found')
        return
    comments = tree.xpath(".//div[@node-type='comment_list']/div")
    if not comments:
        print('comments not found')
        return
    for comment in comments:
        comment_id = comment.xpath(".//@comment_id")
        if comment_id:
            comment_id = comment_id[0]
        else:
            print('comment id not found')
            continue
        context = [
            ''.join(t.itertext()).strip('\n\r\t ')
            for t in comment.xpath(".//div[@class='WB_text']")]
        status_link_id = re.search(
            r'weibo\.com/(.+?)\?',
            doc['collected']['url']
        ).group(1)
        doc_status = db.statuses.find_one({'link_id': status_link_id})
        if not doc_status:
            print('status %s not found' % status_link_id)
            return
        db.comments.update({
            'comment_id': comment_id,
        }, {
            '$set': {
                'keyword': doc_status['keyword'],
                'status_link_id': status_link_id,
                'comment_id': comment_id,
                'context': context,
                'jieba': sum([jieba_cut(t) for t in context], []),
            }
        }, upsert=True)


def run_etl_for_statuses():
    ids = collection.find({'collected.route': 'weibo.search'}).distinct('_id')
    for _id in ids:
        print('etl for weibo search', _id)
        etl_weibo_search(_id)


def run_etl_for_comments():
    ids = collection.find({
        'collected.route': 'weibo.comments',
    }).distinct('_id')
    for _id in ids:
        print('etl for weibo comments', _id)
        etl_weibo_comments(_id)


def main():
    run_etl_for_statuses()
    run_etl_for_comments()


if __name__ == '__main__':
    main()
