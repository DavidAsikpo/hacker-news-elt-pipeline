SELECT 
    id,
    title,
    url,
    CASE WHEN 
         url = '' THEN 'url not found'
         ELSE split_part(REPLACE(CAST(url AS VARCHAR), 'https://', ''), '/', 1)
    END AS domain,
    author,
    created_at,
    updated_at,
    EXTRACT(YEAR FROM created_at) AS YEAR,
    EXTRACT(MONTH FROM created_at)AS MONTH,
    points,
    CASE 
        WHEN points < 1000 then 'below 1000'
        WHEN points <= 2000 AND points > 999  THEN 'above 1000 points'
        WHEN points <= 3000 AND points > 1999 THEN 'above 2000 points'
        WHEN points <= 4400 AND points > 2999 THEN 'above 3000 points'
        ELSE 'above 4400 ponts'
    END AS points_rank,
    num_comments,
    CASE 
        WHEN num_comments < 500 then 'below 500 comments'
        WHEN num_comments <= 1000 AND num_comments > 500  THEN '500 - 1000 comments'
        WHEN num_comments <= 2000 AND num_comments > 1000 THEN '1000 - 2000 comments'
        WHEN num_comments <= 3000 AND num_comments > 2000 THEN '2000 - 3000 comments'
        ELSE 'above 3000 comments'
    END AS comments_rank
FROM
{{ ref('hacker_stg__posts') }}






