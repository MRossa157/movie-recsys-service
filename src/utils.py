import pandas as pd


class MovieEncoder:
    def __init__(self, movie_csv_path) -> None:
        self.movie_data = pd.read_csv(movie_csv_path)

        self.id_to_title = self.movie_data.set_index("movieId")["title"].to_dict()
        self.title_to_id = {v: k for k, v in self.id_to_title.items()}

    def to_idx(self, title):
        return self.title_to_id.get(title, None)

    def to_title(self, idx):
        return self.id_to_title.get(idx, None)

    def num_products(self):
        return self.movie_data.shape[0]


def average_precision(actual, recommended, k=30):
    ap_sum = 0
    hits = 0
    for i in range(k):
        product_id = recommended[i] if i < len(recommended) else None
        if product_id is not None and product_id in actual:
            hits += 1
            ap_sum += hits / (i + 1)
    return ap_sum / min(k, len(actual))


def normalized_average_precision(actual_dict, recommended_dict, k=30):
    total_nap = 0
    users_count = len(actual_dict)

    for user_id, actual in actual_dict.items():
        recommended = recommended_dict.get(user_id, [])

        actual_set = set(actual)
        if len(actual_set) == 0:
            continue

        ap = average_precision(actual_set, recommended, k=k)
        ap_ideal = average_precision(actual_set, list(actual_set)[:k], k=k)

        total_nap += ap / ap_ideal if ap_ideal != 0 else 0

    return total_nap / users_count
