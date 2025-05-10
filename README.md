# PageRank-Algorithm
The PageRank algorithm was created by Google’s co-founders (including Larry Page, for whom the algorithm was named). In PageRank’s algorithm, a website is more important if it is linked to by other important websites, and links from less important websites have their links weighted less. This definition seems a bit circular, but it turns out that there are multiple strategies for calculating these rankings.

<h2>Random Surfer Model</h2>
<p>
  One way to think about PageRank is with the random surfer model, which considers 
  the behavior of a hypothetical surfer on the internet who clicks on links at random. 
  Consider the corpus of web pages below, where an arrow between two pages indicates 
  a link from one page to another.
</p>

<p align="center">
  <img src="https://github.com/Ahnuf-Karim-Chowdhury/PageRank-Algorithm/blob/main/Images/corpus.png?raw=true" alt="Corpus Image">
</p>


<p>
  The random surfer model imagines a surfer who starts with a web page at random, and then randomly chooses links to follow. If the surfer is on Page 2, for example, they would randomly choose between Page 1 and Page 3 to visit next (duplicate links on the same page are treated as a single link, and links from a page to itself are ignored as well). If they chose Page 3, the surfer would then randomly choose between Page 2 and Page 4 to visit next.

A page’s PageRank, then, can be described as the probability that a random surfer is on that page at any given time. After all, if there are more links to a particular page, then it’s more likely that a random surfer will end up on that page. Moreover, a link from a more important site is more likely to be clicked on than a link from a less important site that fewer pages link to, so this model handles weighting links by their importance as well.
</p>


<h2>Markov Chain</h2>
<p>
  One way to interpret this model is as a Markov Chain, where each page represents a state, and each page has a transition model that chooses among its links at random. At each time step, the state switches to one of the pages linked to by the current state.

By sampling states randomly from the Markov Chain, we can get an estimate for each page’s PageRank. We can start by choosing a page at random, then keep following links at random, keeping track of how many times we’ve visited each page. After we’ve gathered all of our samples (based on a number we choose in advance), the proportion of the time we were on each page might be an estimate for that page’s rank.

However, this definition of PageRank proves slightly problematic, if we consider a network of pages like the below.
</p>

<p align="center">
  <img src="https://github.com/Ahnuf-Karim-Chowdhury/PageRank-Algorithm/blob/main/Images/network_disconnected.png?raw=true" alt="Network Disconnected Image">
</p>

<p>
  Imagine we randomly started by sampling Page 5. We’d then have no choice but to go to Page 6, 
  and then no choice but to go to Page 5 after that, and then Page 6 again, and so forth. 
  We’d end up with an estimate of 0.5 for the PageRank for Pages 5 and 6, and an estimate of 0 
  for the PageRank of all the remaining pages, since we spent all our time on Pages 5 and 6 
  and never visited any of the other pages.
</p>

<p>
  To ensure we can always get to somewhere else in the corpus of web pages, we’ll introduce to 
  our model a <strong>damping factor</strong> <code>d</code>. With probability <code>d</code> 
  (where <code>d</code> is usually set around 0.85), the random surfer will choose from one of 
  the links on the current page at random. But otherwise (with probability <code>1 - d</code>), 
  the random surfer chooses one out of all of the pages in the corpus at random 
  (including the one they are currently on).
</p>

<p>
  Our random surfer now starts by choosing a page at random, and then, for each additional sample 
  we’d like to generate, chooses a link from the current page at random with probability 
  <code>d</code>, and chooses any page at random with probability <code>1 - d</code>. 
  If we keep track of how many times each page has shown up as a sample, we can treat the 
  proportion of states that were on a given page as its PageRank.
</p>


<h2>Iterative Algorithm</h2>

<p>
  We can also define a page’s PageRank using a recursive mathematical expression. 
  Let <code>PR(p)</code> be the PageRank of a given page <code>p</code>: the probability that 
  a random surfer ends up on that page. How do we define <code>PR(p)</code>? 
  Well, we know there are two ways that a random surfer could end up on the page:
</p>

<ul>
  <li>With probability <code>1 - d</code>, the surfer chose a page at random and ended up on page <code>p</code>.</li>
  <li>With probability <code>d</code>, the surfer followed a link from a page <code>i</code> to page <code>p</code>.</li>
</ul>

<p>
  The first condition is fairly straightforward to express mathematically: 
  it’s <code>(1 - d) / N</code>, where <code>N</code> is the total number of pages 
  across the entire corpus. This is because the <code>1 - d</code> probability of 
  choosing a page at random is split evenly among all <code>N</code> possible pages.
</p>

<p>
  For the second condition, we need to consider each possible page <code>i</code> 
  that links to page <code>p</code>. For each of those incoming pages, let 
  <code>NumLinks(i)</code> be the number of links on page <code>i</code>. Each page 
  <code>i</code> that links to <code>p</code> has its own PageRank, <code>PR(i)</code>, 
  representing the probability that we are on page <code>i</code> at any given time. 
  And since from page <code>i</code> we travel to any of that page’s links with equal 
  probability, we divide <code>PR(i)</code> by the number of links 
  <code>NumLinks(i)</code> to get the probability that we were on page <code>i</code> 
  and chose the link to page <code>p</code>.
</p>

<p>
  This gives us the following definition for the PageRank for a page <code>p</code>.
</p>

<p align="center">
  <img src="https://github.com/Ahnuf-Karim-Chowdhury/PageRank-Algorithm/blob/main/Images/formula.png?raw=true" alt="Formula Image">
</p>

<p>
  In this formula, <code>d</code> is the damping factor, <code>N</code> is the total number of pages 
  in the corpus, <code>i</code> ranges over all pages that link to page <code>p</code>, and 
  <code>NumLinks(i)</code> is the number of links present on page <code>i</code>.
</p>

<p>
  How would we go about calculating PageRank values for each page, then? We can do so via iteration: 
  start by assuming the PageRank of every page is <code>1 / N</code> 
  (i.e., equally likely to be on any page). Then, use the above formula to calculate new 
  PageRank values for each page, based on the previous PageRank values. 
  If we keep repeating this process, calculating a new set of PageRank values for each page 
  based on the previous set of PageRank values, eventually the PageRank values will converge 
  (i.e., not change by more than a small threshold with each iteration).
</p>

<p>
  In this project, you’ll implement both such approaches for calculating PageRank – calculating 
  both by sampling pages from a Markov Chain random surfer and by iteratively applying 
  the PageRank formula.
</p>


<h2>Instructions for Implementing PageRank</h2>

<h3>1. Implement the <code>transition_model</code> Function</h3>
<p>
  The <code>transition_model</code> function to return a dictionary representing the 
  probability distribution over which page a random surfer would visit next.
</p>
<ul>
  <li><strong>Arguments:</strong>
    <ul>
      <li><code>corpus</code>: A dictionary mapping a page name to a set of pages it links to.</li>
      <li><code>page</code>: The current page (as a string).</li>
      <li><code>damping_factor</code>: A float representing the damping factor.</li>
    </ul>
  </li>
  <li><strong>Return:</strong> A dictionary where each key is a page name and the value is the probability of visiting that page next. All probabilities must sum to 1.</li>
  <li>With probability <code>damping_factor</code>, choose one of the links from the current page at random.</li>
  <li>With probability <code>1 - damping_factor</code>, choose any page in the corpus at random.</li>
  <li>If the current page has no outgoing links, assume it links to all pages in the corpus (including itself).</li>
</ul>

<p><strong>Example:</strong></p>
<pre><code>
corpus = {
  "1.html": {"2.html", "3.html"},
  "2.html": {"3.html"},
  "3.html": {"2.html"}
}
page = "1.html"
damping_factor = 0.85

Output:
{
  "1.html": 0.05,
  "2.html": 0.475,
  "3.html": 0.475
}
</code></pre>

<h3>2. Implement the <code>sample_pagerank</code> Function</h3>
<p>
  Implement the <code>sample_pagerank</code> function to estimate PageRank values using sampling.
</p>
<ul>
  <li><strong>Arguments:</strong>
    <ul>
      <li><code>corpus</code>: A dictionary mapping page names to sets of linked pages.</li>
      <li><code>damping_factor</code>: A float damping factor for the transition model.</li>
      <li><code>n</code>: The number of samples to generate (an integer ≥ 1).</li>
    </ul>
  </li>
  <li><strong>Return:</strong> A dictionary where keys are page names and values are estimated PageRank values based on sampling. The values must sum to 1.</li>
  <li>Start by randomly choosing the first page.</li>
  <li>For each subsequent sample, use the transition model based on the previous page.</li>
  <li>Use the probabilities from <code>transition_model</code> to choose the next sample.</li>
</ul>

<p><strong>Example:</strong></p>
<pre><code>
Transition probabilities = {
  "1.html": 0.05,
  "2.html": 0.475,
  "3.html": 0.475
}
→ Sample "1.html" 5% of the time, "2.html" 47.5%, and "3.html" 47.5%.
</code></pre>

<h3>3. Implement the <code>iterate_pagerank</code> Function</h3>
<p>
  Implement <code>iterate_pagerank</code> to calculate PageRanks using the iterative algorithm.
</p>
<ul>
  <li><strong>Arguments:</strong>
    <ul>
      <li><code>corpus</code>: A dictionary mapping page names to sets of linked pages.</li>
      <li><code>damping_factor</code>: A float damping factor for the PageRank formula.</li>
    </ul>
  </li>
  <li><strong>Return:</strong> A dictionary mapping each page to its PageRank (accurate to within 0.001). The sum of values must be 1.</li>
  <li>Start with each page having rank <code>1 / N</code>, where <code>N</code> is the number of pages.</li>
  <li>Iteratively update PageRank values using the PageRank formula until no value changes by more than 0.001.</li>
  <li>If a page has no outgoing links, assume it links to every page in the corpus (including itself).</li>
</ul>

<h2>Summarizer Version</h2>

<h3>Random Surfer Model</h3>
<ul>
  <li>Imagine a person randomly clicking on links across web pages.</li>
  <li>The probability of being on a page depends on how many other pages link to it.</li>
  <li>Links from important pages carry more weight.</li>
</ul>

<h3>Markov Chain Approach</h3>
<ul>
  <li>Each page is a state, and transitions happen when the surfer clicks links randomly.</li>
  <li>Over time, we estimate how often the surfer lands on each page.</li>
</ul>

<h3>The Problem with Isolated Pages</h3>
<ul>
  <li>If two pages only link to each other, the surfer gets stuck there, making other pages seem irrelevant.</li>
  <li>This creates inaccuracies in ranking.</li>
</ul>

<h3>Introducing Damping Factor (<code>d</code>)</h3>
<ul>
  <li>To prevent getting stuck, a damping factor (typically 0.85) lets the surfer randomly jump to any page sometimes.</li>
  <li>This ensures every page has a chance to be visited.</li>
</ul>

<h3>Iterative Approach to PageRank Calculation</h3>
<ul>
  <li>Initially, all pages have equal rank.</li>
  <li>Update ranks based on incoming links and importance of linking pages.</li>
  <li>Repeat until the ranks stabilize.</li>
</ul>


