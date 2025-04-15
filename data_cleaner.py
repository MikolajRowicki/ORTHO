import os
import json
import csv

def clean_data(data_folder, day_file, first):
    DATA_FOLDER = data_folder
    OUTPUT_FOLDER = "output"
    GAMES_DETAILS_FOLDER = os.path.join(OUTPUT_FOLDER, "games_details")
    GAMES_FOLDER = os.path.join(OUTPUT_FOLDER, "games")

    JSON_FILE = os.path.join(DATA_FOLDER, day_file)

    # Tworzymy foldery, jeśli nie istnieją
    os.makedirs(GAMES_DETAILS_FOLDER, exist_ok=True)
    os.makedirs(GAMES_FOLDER, exist_ok=True)

    # Wczytujemy plik JSON
    with open(JSON_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Plik zbiorczy dla Track_Results
    games_file_path = os.path.join(GAMES_FOLDER, "games.csv")

    # Nagłówki plików
    headers = [
        "ID", "Date", "Consent", "Team_Name", "Selected_Language",
        "Consent_Time_X_axis", "Age_X_axis", "Companionship_X_axis", "Question_Time_X_axis",
        "Consent_Time_Y_axis", "Age_Y_axis", "Companionship_Y_axis", "Question_Time_Y_axis",
        "StartTime", "ClosingTime", "Completed", "TerminationType",
        "Track_ID", "Difficulty_Level", "Track_StartTime", "Track_ClosingTime",
        "Track_Time", "Mistake", "Track_Completed", "Interface_Mode", "GAME_ID"
    ]
    k = 0
    # Otwieramy oba pliki do zapisu
    with open(games_file_path, mode="a", newline="", encoding="utf-8") as games_file:
        
        games_writer = csv.writer(games_file)
        if first:
            # Zapisujemy nagłówki
            games_writer.writerow(headers)

        # Iterujemy przez wszystkie sesje
        for session in data.get("Sessions_List", []):
            session_id = session.get("ID", "unknown")
            team_name = session.get("Team_Name", "unknown").replace(" ", "")  # Usuwamy spacje
            
            # Iterujemy przez każdy Track_Results w sesji
            for track in session.get("Track_Results", []):
                track_id = track.get("Track_ID", "unknown")
                start_time = track.get("StartTime", "unknown").replace(":", "-")  # Formatowanie czasu

                # Tworzymy nazwę pliku CSV dla punktów
                file_name = f"{session_id}_{team_name}_{track_id}_{start_time}.csv"
                file_path = os.path.join(GAMES_DETAILS_FOLDER, file_name)

                # Pobieramy punkty
                points = track.get("Points", [])

                # Zapisujemy do CSV z punktami
                with open(file_path, mode="w", newline="", encoding="utf-8") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["X", "Y", "Time", "Status", "GAME_ID"])  # Nagłówki kolumn
                    for point in points:
                        writer.writerow([
                            point.get("X", ""),
                            point.get("Y", ""),
                            point.get("Time", ""),
                            point.get("Status", ""),
                            f"{session_id}_{team_name}_{track_id}_{start_time}"
                        ])

                print(f"Zapisano plik: {file_name}")

                # Tworzymy wiersz z danymi sesji i ścieżki
                row = [
                    session.get("ID", ""),
                    session.get("Date", ""),
                    session.get("Consent", ""),
                    session.get("Team_Name", ""),
                    session.get("Selected_Language", ""),
                    session.get("Consent_Time_X_axis", ""),
                    session.get("Age_X_axis", ""),
                    session.get("Companionship_X_axis", ""),
                    session.get("Question_Time_X_axis", ""),
                    session.get("Consent_Time_Y_axis", ""),
                    session.get("Age_Y_axis", ""),
                    session.get("Companionship_Y_axis", ""),
                    session.get("Question_Time_Y_axis", ""),
                    session.get("StartTime", ""),
                    session.get("ClosingTime", ""),
                    session.get("Completed", ""),
                    session.get("TerminationType", ""),
                    track.get("Track_ID", ""),
                    track.get("Difficulty_Level", ""),
                    track.get("StartTime", ""),
                    track.get("ClosingTime", ""),
                    track.get("Time", ""),
                    track.get("Mistake", ""),
                    track.get("Completed", ""),
                    str(track.get("Interface_Mode", [])),  # Konwertujemy listę na string
                    f"{session_id}_{team_name}_{track_id}_{start_time}"
                ]

                # Zapisujemy do plików
                games_writer.writerow(row)

    
    
def clean_all_data():
    first = True
    for file in os.listdir("data"):
        if file.endswith(".json"):
            clean_data("data", file, first)
            print(f"Przetworzono plik: {file}")
            first = False
    print("Konwersja JSON → CSV zakończona!")    


clean_all_data()
