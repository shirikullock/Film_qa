import sys
import question
import crawler


def main(argv):
    if argv[1] == 'create':
        crawler.start_to_crawl()
    if argv[1] == 'question':
        question.question_manager(argv[2])
    exit(0)


if __name__ == '__main__':
    main(sys.argv)