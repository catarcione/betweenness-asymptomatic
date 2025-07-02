from sklearn.metrics import roc_auc_score, roc_curve

def auc_score(infected_nodes, centrality_measures, observed_nodes):
    """
    Calculate the AUC score and ROC curve, given the set of infected nodes,
    the network centrality measure used for ranking, and a list of observed 
    nodes to be excluded from the calculation.

    Parameters:
    - infected_nodes: List of infected nodes
    - centrality_measures: Dictionary where the keys are node indices and
                           the values are their corresponding centrality
                           measures (e.g., degree, betweenness, etc.)
    - observed_nodes : List of node indices to exclude from evaluation
    
    Returns:
    - auc: The Area Under the Curve (AUC) score
    - curve: Tuple containing the False Positive Rate (FPR),
             True Positive Rate (TPR), and thresholds for
             plotting the ROC curve
    """
    # Filter out observed nodes
    evaluation_nodes = [node for node in centrality_measures if node not in observed_nodes]

    # Build ground truth and scores
    y_true = []
    y_scores = []

    for node in evaluation_nodes:
        y_true.append(1 if node in infected_nodes else 0)
        y_scores.append(centrality_measures[node])

    # Compute the AUC score
    auc = roc_auc_score(y_true, y_scores)
    # Compute the ROC curve
    curve = roc_curve(y_true, y_scores)

    return {'auc': auc, 'roc': curve}