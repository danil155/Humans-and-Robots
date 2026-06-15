import { useState } from "react";
import { useSolver } from "./hooks/useSolver";
import { ParamsPanel, ResultPanel } from "./components/features";
import { DEFAULT_PRODUCTION_PARAMS, DEFAULT_GAME_PARAMS } from "./constants/gameConfig";
import "./App.css";

export default function App() {
  const [prodParams, setProdParams] = useState(DEFAULT_PRODUCTION_PARAMS);
  const [gameParams, setGameParams] = useState(DEFAULT_GAME_PARAMS);

  const { result, loading, error, solve } = useSolver();

  const handleProdChange = (key, val) =>
      setProdParams((p) => ({ ...p, [key]: val }));

  const handleGameChange = (key, val) =>
      setGameParams((p) => ({ ...p, [key]: val }));

  const handleSolve = () => solve(prodParams, gameParams);

  return (
      <div className="app-layout">
        <h1 className="sr-only">
          Люди и роботы
        </h1>

        <ParamsPanel
            prodParams={prodParams}
            gameParams={gameParams}
            onProdChange={handleProdChange}
            onGameChange={handleGameChange}
            onSolve={handleSolve}
            loading={loading}
        />

        <ResultPanel
            result={result}
            loading={loading}
            error={error}
        />
      </div>
  );
}
