SELECT 
    id, downvotes_from_actions, upvotes_from_actions, active
FROM 
    member
WHERE 
    (downvotes_from_actions - upvotes_from_actions) > 0
ORDER BY 
    (downvotes_from_actions - upvotes_from_actions) DESC;