from functools import partial
from operator import is_not
from typing import Any

from google.oauth2 import service_account
from googleapiclient.discovery import build


def get_game_name(row: list) -> str | None:
    if len(row) != 0 and row[0] and len(row[0]) != 0:
        return row[0]
    else:
        return None


def get_another_game_info(row: list) -> list:
    row[0] = None

    return list(filter(partial(is_not, None), row))


def get_prepared_row(row: list):
    game_name: str = get_game_name(row)

    another_game_info: list = get_another_game_info(row)

    if game_name:
        if len(another_game_info) == 0:
            return game_name
        else:
            another_game_info_str = ''.join([' ('] + another_game_info + [')'])

            if (100 - len(game_name) - len(another_game_info_str)) >= 0:
                return game_name + another_game_info_str
            else:
                return game_name
    else:
        return None


def prepare_row_for_result(row_data: list) -> str | None:
    if row_data:
        return get_prepared_row(row_data)
    else:
        return None


def create_creds() -> Any:
    return (service_account
    .Credentials
    .from_service_account_file(
        "credentials.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]))


def get_sheet_rows_from_google_sheets(sample_spreadsheet_id: str, rng: str) -> list:
    service = build("sheets", "v4", credentials=create_creds())

    sheet = service.spreadsheets()

    result = sheet.values().get(spreadsheetId=sample_spreadsheet_id, range=rng).execute()

    return result.get('values', [])


def create_result(rows_data: list) -> list:
    result = []

    for row_data in rows_data:
        prepared_row = prepare_row_for_result(row_data)

        if prepared_row:
            result.append(prepared_row)

    return result


def get_games_list(sample_spreadsheet_id: str, rng: str) -> list | None:
    rows_data = get_sheet_rows_from_google_sheets(sample_spreadsheet_id, rng)

    if rows_data:
        return create_result(rows_data)
    else:
        return None
