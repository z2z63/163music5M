SELECT (SELECT COUNT(*) FROM user_song)    AS '评论数量',
       (SELECT COUNT(*) FROM user)         AS '用户数量',
       (SELECT COUNT(*) FROM artist)       AS '歌手数量',
       (SELECT COUNT(*) FROM song)         AS '歌曲数量',
       (SELECT AVG(t3.count_per_user) AS '每个用户平均评论歌曲数量'
        FROM (SELECT user_163_id, COUNT(*) AS 'count_per_user'
              FROM (SELECT user.user_163_id, song_163_id
                    FROM user
                             JOIN (SELECT user_163_id, song_163_id
                                   from user_song
                                   GROUP BY user_163_id, song_163_id) AS t1
                                  ON user.user_163_id = t1.user_163_id) AS t2
              GROUP BY user_163_id) AS t3) AS '每个用户平均评论歌曲数量'