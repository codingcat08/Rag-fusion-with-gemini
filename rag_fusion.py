import os
import random
import google.generativeai as genai
genai.configure(api_key="PUT YOUR API KEY HERE")
original_query1 = "impact of climate change"
def generate_queries(original_query) :
    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat(
    history=[
        {"role": "model", "parts": "You are a helpful assistant that generates multiple search queries based on a single input query."},
        {"role": "user", "parts": f"Generate multiple search queries related to: {original_query}"},
    ]
    )
    response = chat.send_message("OUTPUT (4 queries):")
    return response.text.strip().split("\n")
    #print(response.text)
generate_queries(original_query1) 
def vector_search(query, all_documents):
    available_docs = list(all_documents.keys())
    random.shuffle(available_docs)
    selected_docs = available_docs[:random.randint(2, 5)]
    scores = {doc: round(random.uniform(0.7, 0.9), 2) for doc in selected_docs}
    return {doc: score for doc, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)}

# Reciprocal Rank Fusion algorithm
def reciprocal_rank_fusion(search_results_dict, k=60):
    fused_scores = {}
    print("Initial individual search result ranks:")
    for query, doc_scores in search_results_dict.items():
        print(f"For query '{query}': {doc_scores}")
        
    for query, doc_scores in search_results_dict.items():
        for rank, (doc, score) in enumerate(sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)):
            if doc not in fused_scores:
                fused_scores[doc] = 0
            previous_score = fused_scores[doc]
            fused_scores[doc] += 1 / (rank + k)
            print(f"Updating score for {doc} from {previous_score} to {fused_scores[doc]} based on rank {rank} in query '{query}'")

    reranked_results = {doc: score for doc, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)}
    print("Final reranked results:", reranked_results)
    return reranked_results

# Dummy function to simulate generative output
def generate_output(reranked_results, queries):
    return f"Final output based on {queries} and reranked documents: {list(reranked_results.keys())}"


# Predefined set of documents (usually these would be from your search database)
all_documents = {
    "doc1": "Climate change and economic impact.",
    "doc2": "Public health concerns due to climate change.",
    "doc3": "Climate change: A social perspective.",
    "doc4": "Technological solutions to climate change.",
    "doc5": "Policy changes needed to combat climate change.",
    "doc6": "Climate change and its impact on biodiversity.",
    "doc7": "Climate change: The science and models.",
    "doc8": "Global warming: A subset of climate change.",
    "doc9": "How climate change affects daily weather.",
    "doc10": "The history of climate change activism."
}

# Main function
if __name__ == "__main__":
    original_query = "impact of climate change"
    generated_queries = generate_queries(original_query)
    
    all_results = {}
    for query in generated_queries:
        search_results = vector_search(query, all_documents)
        all_results[query] = search_results
    
    reranked_results = reciprocal_rank_fusion(all_results)
    
    final_output = generate_output(reranked_results, generated_queries)
    print("the final output is -> ")
    print(final_output)   