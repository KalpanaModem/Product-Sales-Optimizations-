function compareAlgorithms() {
  const selected = document.getElementById("productSelect").value;

  const map = buildAssociationMap();
  const related = map[selected] || {};
  const acoScore = Object.values(related)
    .sort((a, b) => b - a)
    .slice(0, 5)
    .reduce((sum, value) => sum + value, 0);

  const products = getAllProducts();
  let population = Array.from({ length: 10 }, () => randomBundle(products));

  for (let i = 0; i < 10; i++) {
    population.sort((a, b) => fitness(b) - fitness(a));
    population = population.slice(0, 5);
  }

  const best = population[0];
  const gaScore = fitness(best);

  const psoScore = (Math.random() + Math.random() + Math.random()) * 100;

  const scores = [
    { name: "ACO", score: acoScore },
    { name: "GA", score: gaScore },
    { name: "PSO", score: psoScore }
  ];

  scores.sort((a, b) => b.score - a.score);
  const winner = scores[0];

  let result = document.getElementById("acoOutput").textContent;

  result += `\n\n===== FINAL COMPARISON =====\n`;
  result += `ACO Score: ${acoScore.toFixed(2)}\n`;
  result += `GA Score: ${gaScore.toFixed(2)}\n`;
  result += `PSO Score: ${psoScore.toFixed(2)}\n\n`;
  result += `?? BEST: ${winner.name}\n`;

  document.getElementById("acoOutput").textContent = result;
}
