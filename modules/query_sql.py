# Профиль пользователя model.Profiles + текущий вес model.UserWeight

join_Pf_Uw = """
    SELECT p.*, uw.real_weight 
    FROM user_weight 
    AS uw 
    JOIN profiles 
    AS p 
    ON uw.user_id  = p.user_id 
    WHERE uw.user_id = 1 
    ORDER BY uw.created_at 
    DESC LIMIT 1
"""

