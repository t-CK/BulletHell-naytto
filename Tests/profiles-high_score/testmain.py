from profiles import Profiles, High_Score

if __name__ == "__main__":
    hs = High_Score()
    hs.add_score("Testi", 10, 100, 5.0)
    hs.add_score("sdlkfj", 58, 150, 8.5)
    print(hs.get_scores())