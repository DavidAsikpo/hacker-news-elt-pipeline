SELECT 
    CAST(id AS INTEGER) AS id,
    CAST(title AS VARCHAR) AS title,
    CASE WHEN 
        CAST(url AS VARCHAR) = '' THEN 'url not found'
        ELSE CAST(url AS VARCHAR)
    END AS url,
    CASE WHEN 
         CAST(author AS VARCHAR) = '' THEN 'authot not found'
         ELSE CAST(author AS VARCHAR)
    END AS author,
    CASE WHEN 
         CAST(created_at AS TIMESTAMP) is NULL THEN NULL
         ELSE CAST(created_at AS TIMESTAMP)
    END AS created_at,
    CASE WHEN 
         CAST(updated_at AS TIMESTAMP) is NULL THEN NULL
         ELSE CAST(updated_at AS TIMESTAMP)
    END AS updated_at,
    CASE WHEN 
         CAST(points AS INTEGER) is NULL THEN NULL
         ELSE CAST(points AS INTEGER)
    END AS points,
    CASE WHEN 
         CAST(num_comments AS INTEGER) is NULL THEN NULL
         ELSE CAST(num_comments AS INTEGER)
    END AS num_comments
FROM
{{ source('raw_data', 'hack_stories') }}




