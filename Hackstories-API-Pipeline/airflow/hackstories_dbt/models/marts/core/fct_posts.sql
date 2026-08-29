{{ config(materialized = 'incremental',
          incremental_strategy = 'merge',
          unique_key = 'post_id'
          )
}}

{% set incremental_col = 'created_at' %}

SELECT
    id AS post_id,
    {{ dbt_utils.generate_surrogate_key(['author']) }} AS author_id,
    domain,
    points,
    points_rank,
    num_comments,
    comments_rank,
    created_at,
    updated_at
FROM {{ ref('int_posts') }}
{% if is_incremental() %}
WHERE {{ incremental_col }} > (select COALESCE(MAX({{ incremental_col }}), '1900-01-01') FROM {{ this }})
{% endif %}