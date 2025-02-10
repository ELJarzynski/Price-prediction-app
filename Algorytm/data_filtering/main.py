from data_filtering.data_loader import *
import pandas as pd

class HousingDataProcessor:
    def __init__(self, df, start_year, end_year):
        # Przypisujemy przekazany DataFrame i zakres lat
        self.data = df
        self.start_year = start_year
        self.end_year = end_year

    def filter_by_decade(self):
        # Filtracja danych tylko dla wybranej dekady
        self.data = self.data[(self.data['YearBuilt'] >= self.start_year) & (self.data['YearBuilt'] <= self.end_year)]

    def split_by_years(self):
        # Podział dekady na 3 okresy lat
        period_length = (self.end_year - self.start_year + 1) // 3
        self.data_period_1 = self.data[self.data['YearBuilt'] <= self.start_year + period_length - 1]
        self.data_period_2 = self.data[(self.data['YearBuilt'] > self.start_year + period_length - 1) & (
                    self.data['YearBuilt'] <= self.start_year + 2 * period_length - 1)]
        self.data_period_3 = self.data[self.data['YearBuilt'] > self.start_year + 2 * period_length - 1]

    def process_decade_data(self, df, years_label):
        results = []
        # Grupowanie według lokalizacji
        for location, location_df in df.groupby('Neighborhood'):
            # Grupowanie według liczby sypialni i łazienek
            for (bedrooms, bathrooms), bed_bath_df in location_df.groupby(['Bedrooms', 'Bathrooms']):
                # Znalezienie minimalnej wartości SquareFeet dla ustalenia początkowego zakresu
                min_square_feet = bed_bath_df['SquareFeet'].min()

                # Tworzenie przedziałów dynamicznie zaczynających się od minimalnego SquareFeet
                bins = list(range(min_square_feet, bed_bath_df['SquareFeet'].max() + 20, 20))
                bed_bath_df['SquareFeetRange'] = pd.cut(bed_bath_df['SquareFeet'], bins=bins, right=False)

                # Grupowanie według przedziałów i liczenie średniej ceny oraz powierzchni
                grouped_df = bed_bath_df.groupby('SquareFeetRange').agg(
                    AverageSquareFeet=('SquareFeet', 'mean'),
                    AveragePrice=('Price', 'mean')
                ).reset_index()

                # Usunięcie wierszy, gdzie AveragePrice jest zerowe
                grouped_df = grouped_df[grouped_df['AveragePrice'] > 0]

                # Dodanie kolumny z etykietą dla łatwiejszej identyfikacji
                grouped_df['Label'] = f"{years_label}_{location}_bed{bedrooms}_bath{bathrooms}"

                # Dodanie kolumn do identyfikacji (Neighborhood, Bedrooms, Bathrooms)
                grouped_df['Neighborhood'] = location
                grouped_df['Bedrooms'] = bedrooms
                grouped_df['Bathrooms'] = bathrooms

                # Przechowywanie roku budowy
                grouped_df['YearBuilt'] = bed_bath_df['YearBuilt'].iloc[0]  # We keep the year from the first row

                # Dodanie oczyszczonych wyników
                results.append(self.remove_unrealistic_prices(grouped_df))

        return pd.concat(results, ignore_index=True)

    def remove_unrealistic_prices(self, df):
        # Sortujemy przedziały malejąco według AverageSquareFeet
        df = df.sort_values(by='AverageSquareFeet', ascending=False).reset_index(drop=True)

        while True:
            to_drop = []
            keep_mask = [True] * len(df)  # Array to keep track of which rows to keep

            for i in range(len(df) - 3):
                prices = df.loc[i:i + 3, 'AveragePrice'].values

                # Sprawdzenie, czy ceny są w malejącej kolejności
                if all(prices[j] > prices[j + 1] for j in range(len(prices) - 1)):
                    continue

                # Sprawdzanie, który wiersz należy usunąć
                for j in range(4):
                    if (j == 0 and prices[j] < max(prices[1:])) or \
                            (j == 1 and prices[j] > prices[0] and prices[j] < max(prices[[0, 2, 3]])) or \
                            (j == 2 and prices[j] > prices[0] and prices[j] < max(prices[[1, 3]])) or \
                            (j == 3 and prices[j] < min(prices[:3])):
                        keep_mask[i + j] = False  # Mark for removal

            # Usuwanie oznaczonych wierszy
            if any(not keep for keep in keep_mask):
                df = df[keep_mask].reset_index(drop=True)
            else:
                break  # Koniec pętli, gdy nie ma więcej do usunięcia

        return df

    def process_all(self):
        # Uruchamiamy pełne przetwarzanie
        self.filter_by_decade()
        self.split_by_years()

        # Procesujemy dla każdego z przedziałów lat
        df_period_1 = self.process_decade_data(self.data_period_1,
                                               f'{self.start_year}-{self.start_year + (self.end_year - self.start_year) // 3}')
        df_period_2 = self.process_decade_data(self.data_period_2,
                                               f'{self.start_year + (self.end_year - self.start_year) // 3 + 1}-{self.start_year + 2 * (self.end_year - self.start_year) // 3}')
        df_period_3 = self.process_decade_data(self.data_period_3,
                                               f'{self.start_year + 2 * (self.end_year - self.start_year) // 3 + 1}-{self.end_year}')

        # Łączymy wyniki w jeden DataFrame
        self.result = pd.concat([df_period_1, df_period_2, df_period_3], ignore_index=True)

        # Usunięcie kolumny Label
        self.result = self.result.drop(columns=['Label'])

        # Sortujemy wynik według AverageSquareFeet
        self.result = self.result.sort_values(by='AverageSquareFeet').reset_index(drop=True)

        return self.result

    def save_result(self, output_path):
        # Zapisujemy wynikowy DataFrame do pliku CSV
        self.result.to_csv(output_path, index=False)

# Przykład użycia:
processor = HousingDataProcessor(df, start_year=2020, end_year=2022)
wynik_df = processor.process_all()
processor.save_result("dekada2020-2024.csv")
file_directory = r"../datasets/decades/dekada1960-1969.csv"
df = pd.read_csv(file_directory)
print(df[(df['Neighborhood'] == 'Rural') & (df['Bedrooms'] == 2) & (df['Bathrooms'] == 2)].sort_values(by='YearBuilt'))
