# This is a sample Python script.
import argparse
import logging
import os

from prompt_toolkit import print_formatted_text, HTML, PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from prompt_toolkit.shortcuts import ProgressBar

from app.data.data_service import DataService
from app.input_controller import InputController
from app.log_handler import LogHandler
from app.module_mgmt.module_manager import ModuleManager
from app.output.excel_output_handler import ExcelOutputHandler
from app.output.prompt_output_handler import PromptOutputHandler

HISTORY_FILE = '.oscar_history'

DEFAULT_CONFIG_DIR_NAME = "mod_conf"


def parse_arguments():
    parser = argparse.ArgumentParser(description='Fetches HAL bibliographic references in CSV format.')
    parser.add_argument('--conf_dir', dest='conf_dir',
                        help='Output directory', required=False, default=DEFAULT_CONFIG_DIR_NAME)
    parser.add_argument('--manual', action='store_true', help='Manual mode (command line)')
    parser.add_argument('--command', dest='command',
                        help='Command for automatic mode', required=False)
    return parser.parse_args()


TEXT_STATUS = {
    'success': "lightseagreen",
    'error': "indianred",
    'info': "lightskyblue",
}


def print_with_status(text: str, status: str):
    assert status in TEXT_STATUS
    print_formatted_text(HTML(f"<{TEXT_STATUS[status]}>{text}</{TEXT_STATUS[status]}>"))


def error_printer(text: str):
    print_with_status(text=text, status="error")


def success_printer(text: str):
    print_with_status(text=text, status="success")


def info_printer(text: str):
    print_with_status(text=text, status="info")


def main(args):
    module_manager = ModuleManager(conf_dir=args.conf_dir)
    data_service = DataService(module_manager=module_manager)
    if args.manual:
        output_handler = PromptOutputHandler()
    else:
        logger = LogHandler(logger_name='compare_sources', dir_name='log', file_name='compare_sources.log',
                            level=logging.INFO).create_rotating_log()
        output_handler = ExcelOutputHandler()
    if args.manual:
        controller = InputController(data_service=data_service, output_handler=output_handler,
                                     error_logger=error_printer, info_logger=info_printer,
                                     success_logger=success_printer)
        iter_init = controller.iterative_initializer()
        first = True
        with ProgressBar(title="Initialisation des modules") as progress_bar:
            progress_bar.title = "Initialisation :"
            for _ in progress_bar(range(module_manager.nb_modules), label="Initialisation"):
                if not first:
                    progress_bar.title += " ** "
                else:
                    first = False
                progress_bar.title += f" {next(iter_init)}"
    else:
        controller = InputController(data_service=data_service, output_handler=output_handler,
                                     error_logger=logger.error, info_logger=logger.info, success_logger=logger.info)
        list(controller.iterative_initializer())

    if args.manual:
        user_input_loop(controller)
    elif args.command:
        controller.handle(user_input=args.command, entity_type='structure')


def user_input_loop(controller: InputController):
    file = f"{os.path.expanduser('~')}/{HISTORY_FILE}"
    with open(file, 'a', encoding='utf-8') as _:
        pass
    session = PromptSession(history=FileHistory(file))
    toolbar = HTML(
        '<b><style bg="ansired">A</style></b> pour acronyme, <b><style bg="ansired">N</style></b> pour numéro, <b><style bg="ansired">C</style></b> pour id rnsr, <b><style bg="ansired">T</style></b> pour intitulé <b><style bg="ansired">=</style></b> valeur | <b><style bg="ansired">Q</style></b> pour quitter')
    try:
        while 1:
            answer = session.prompt(
                ">",
                auto_suggest=AutoSuggestFromHistory(),
                bottom_toolbar=toolbar)
            try:
                controller.handle(user_input=answer, entity_type="structure")
            except ValueError:
                print_formatted_text(HTML('<red>Choix non compris</red>'))
    except KeyboardInterrupt:
        print_formatted_text(HTML('<red>Interruption utilisateur</red>'))


if __name__ == '__main__':
    main(parse_arguments())
