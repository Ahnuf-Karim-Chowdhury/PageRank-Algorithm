import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.
    """
    total_pages = len(corpus)
    probability_distribution = dict()

    links = corpus[page]
    if links:
        for p in corpus:
            probability_distribution[p] = (1 - damping_factor) / total_pages
        for linked_page in links:
            probability_distribution[linked_page] += damping_factor / len(links)
    else:
        # If page has no links, treat it as linking to all pages (including itself)
        for p in corpus:
            probability_distribution[p] = 1 / total_pages

    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.
    """
    page_rank = {page: 0 for page in corpus}
    current_page = random.choice(list(corpus.keys()))

    for _ in range(n):
        page_rank[current_page] += 1
        distribution = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(
            population=list(distribution.keys()),
            weights=list(distribution.values()),
            k=1,
        )[0]

    # Normalize so that PageRanks sum to 1
    for page in page_rank:
        page_rank[page] /= n

    return page_rank


def iterate_pagerank(corpus, damping_factor, threshold=0.001):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.
    """
    total_pages = len(corpus)
    pagerank = {page: 1 / total_pages for page in corpus}

    # Fix pages with no links: treat them as linking to all pages
    fixed_corpus = {
        page: (links if links else set(corpus.keys())) for page, links in corpus.items()
    }

    converged = False
    while not converged:
        new_rank = {}
        for page in corpus:
            rank_sum = 0
            for possible_page in corpus:
                if page in fixed_corpus[possible_page]:
                    rank_sum += pagerank[possible_page] / len(
                        fixed_corpus[possible_page]
                    )
            new_rank[page] = (
                1 - damping_factor
            ) / total_pages + damping_factor * rank_sum

        converged = all(
            abs(new_rank[page] - pagerank[page]) < threshold for page in pagerank
        )
        pagerank = new_rank

    return pagerank


if __name__ == "__main__":
    main()
