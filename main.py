import math


def poisson_prob(k, lambd):
  """Calcule la probabilité exacte d'avoir k corners avec une moyenne lambd."""
  return (lambd**k * math.exp(-lambd)) / math.factorial(k)


def calculer_lambda_avec_gamestate(
    lambda_base, prob_gagner, prob_nul, prob_perdre
):
  """Ajuste le lambda offensif d'une équipe en fonction

  du scénario de match (Gagner, Nul, Perdre).
  """
  coef_en_mene = 1.20  # Mené = pousse plus (+20% de corners)
  coef_en_nul = 1.00  # Neutre
  coef_en_gagne = 0.85  # Gagne = gère le score (-15% de corners)

  facteur_ajustement = (
      (prob_perdre * coef_en_mene)
      + (prob_nul * coef_en_nul)
      + (prob_gagner * coef_en_gagne)
  )

  return lambda_base * facteur_ajustement


def analyser_corners_avec_gamestate(
    lambda_A_base,
    lambda_B_base,
    prob_A_gagne,
    prob_match_nul,
    prob_B_gagne,
    ligne_bookmaker,
):
  # Application de la pondération Game State
  lambda_A_final = calculer_lambda_avec_gamestate(
      lambda_A_base, prob_A_gagne, prob_match_nul, prob_B_gagne
  )
  lambda_B_final = calculer_lambda_avec_gamestate(
      lambda_B_base, prob_B_gagne, prob_match_nul, prob_A_gagne
  )

  max_corners = 20
  prob_totale_over = 0.0
  prob_totale_under = 0.0

  for corners_A in range(max_corners):
    p_A = poisson_prob(corners_A, lambda_A_final)
    for corners_B in range(max_corners):
      p_B = poisson_prob(corners_B, lambda_B_final)

      prob_exacte = p_A * p_B
      total_corners = corners_A + corners_B

      if total_corners > ligne_bookmaker:
        prob_totale_over += prob_exacte
      elif total_corners < ligne_bookmaker:
        prob_totale_under += prob_exacte

  cote_over = 1 / prob_totale_over if prob_totale_over > 0 else 99.0
  cote_under = 1 / prob_totale_under if prob_totale_under > 0 else 99.0

  print("=== RÉSULTATS (AVEC GAME STATE) ===")
  print(
      f"Lambda ajusté A : {lambda_A_final:.2f} | Lambda ajusté B:"
      f" {lambda_B_final:.2f}"
  )
  print(
      f"Probabilité Over {ligne_bookmaker} : {prob_totale_over*100:.2f}% | Cote"
      f" équitable : {cote_over:.2f}"
  )
  print(
      f"Probabilité Under {ligne_bookmaker} : {prob_totale_under*100:.2f}% | Cote"
      f" équitable : {cote_under:.2f}"
  )


# --- EXEMPLE D'UTILISATION ---
# 1. Moyennes de base des équipes (Domicile et Extérieur)
lam_A_base = 5.8
lam_B_base = 3.6

# 2. Probabilités du match 1X2 (ex: Domicile 55%, Nul 25%, Extérieur 20%)
p_dom = 0.55
p_nul = 0.25
p_ext = 0.20

# 3. Ligne du bookmaker
ligne = 9.5

# Exécution du calcul
analyser_corners_avec_gamestate(
    lam_A_base, lam_B_base, p_dom, p_nul, p_ext, ligne
)
