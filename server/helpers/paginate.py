def paginate(rank: str, data, limit: int, start: int):
    filtered_data = data[start - 1 : start + limit - 1]

    prev_lim = min(limit, start - 1)
    prev_start = min(abs(start - limit), 1)
    prev = (
        None if start == 1 else f"/api/rank/{rank}?limit={prev_lim}&start={prev_start}"
    )

    next_start = start + limit
    next_lim = min(limit, len(data) - next_start + 1)
    next = (
        None
        if start + limit - 1 >= len(data)
        else f"/api/rank/{rank}?limit={next_lim}&start={next_start}"
    )

    return {
        "ranking": rank,
        "limit": limit,
        "start": start,
        # "games": filtered_data,
        "games": [item["id"] for item in filtered_data],
        "prev": prev,
        "next": next,
    }
