SELECT 
    DISTINCT {{ dbt_utils.generate_surrogate_key(['author']) }} AS author_id,
    author AS author_name,
    min(created_at) AS first_post
FROM {{ ref('int_posts') }}
GROUP BY author


