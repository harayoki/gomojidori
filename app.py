from gomojidori import run_ui, get_arg_parser, DEFAULT_INPUT

parser = get_arg_parser()
args = parser.parse_args()
args.input = DEFAULT_INPUT

run_ui(args)
