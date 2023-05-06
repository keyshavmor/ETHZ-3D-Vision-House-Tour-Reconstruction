from sentence_transformers import SentenceTransformer
import numpy as np

# Load the pre-trained model
model = SentenceTransformer('bert-base-nli-mean-tokens')

# Encode the specific terms and the general terms
# Read the contents of subtitles_labels (labels from the subtitles) into a list
with open('subtitles_labels.txt', 'r') as f:
    specific_terms = f.read().splitlines()

# Read the contents of file2 (labels from the ADE20K) into a list
with open('ADE20K_labels.txt', 'r') as f:
    general_terms = f.read().splitlines()

specific_term_embeddings = model.encode(specific_terms)
general_term_embeddings = model.encode(general_terms)

# Calculate the cosine similarity between the specific term and each general term
similarities = np.dot(specific_term_embeddings, general_term_embeddings.T) / (np.linalg.norm(specific_term_embeddings, axis=1)[:, None] * np.linalg.norm(general_term_embeddings, axis=1))
best_match_indices = np.argmax(similarities, axis=1)

# Output the best matching general term for each specific term
with open('results.txt', 'w') as f:
    for i, term in enumerate(specific_terms):
        if (max(similarities[i]) < 0.8):
            note = " --- probably not mentioned in video"
        else:
            note = ""
        result = f'{term} --> {general_terms[best_match_indices[i]]} {note}'
        
        f.write(result + '\n')

