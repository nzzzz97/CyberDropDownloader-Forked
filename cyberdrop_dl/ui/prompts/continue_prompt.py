from InquirerPy import inquirer


def enter_to_continue() -> None:
    inquirer.text(
        message="press enter to continue",
    ).execute()
