from profiles import Profiles, High_Score

if __name__ == "__main__":
    hs = High_Score()
    hs.add_score("Testi", 10, 100, 5.0)
    hs.add_score("sdlkfj", 58, 150, 8.5)
    print("CASE 1:\n", hs.get_scores(), "\n")
    hs.update_score("Testi", 50, 200, 20.5)
    print("CASE 2\n", hs.get_scores())