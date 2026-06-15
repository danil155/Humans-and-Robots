import { Section, EmptyState, ErrorBanner, RawJsonPanel } from "../../ui";
import { EquilibriumPath } from "./EquilibriumPath/EquilibriumPath";
import { PayoffCards } from "./PayoffCards/PayoffCards";
import { FirmBranch } from "./FirmBranch/FirmBranch";
import { InterpretationSection } from "./InterpretationSection/InterpretationSection";
import { SensitivitySection } from "./SensitivitySection/SensitivitySection";
import "./ResultPanel.css";

export function ResultPanel({ result, loading, error }) {
    return (
        <main className="result-panel">
            <header className="result-panel__header">
                <p className="result-panel__title">Результат</p>
                <p className="result-panel__subtitle">Совершенное в подиграх равновесие</p>
            </header>

            {/* ── States ── */}
            {!result && !loading && !error && (
                <EmptyState message="Заполните параметры и нажмите «Построить равновесие»" />
            )}

            {loading && (
                <EmptyState
                    icon="ti-loader-2 spin"
                    message="Решаем задачу ЛП и строим дерево игры..."
                />
            )}

            {error && <ErrorBanner message={error} />}

            {/* ── Result sections ── */}
            {result && (
                <>
                    {/* Nash equilibrium */}
                    <Section title="Равновесие по Нэшу (совершенное в подиграх)">
                        <EquilibriumPath path={result.equilibrium} />

                        {result.payoffs && (
                            <div className="result-panel__payoffs-block">
                                <p className="result-panel__sub-label">Выигрыши в равновесии</p>
                                <PayoffCards payoffs={result.payoffs} />
                            </div>
                        )}
                    </Section>

                    {/* Game tree */}
                    {result.full_tree_eval && (
                        <Section title="Дерево игры">
                            {Object.entries(result.full_tree_eval).map(([firmKey, branch]) => (
                                <FirmBranch key={firmKey} firmKey={firmKey} branch={branch} />
                            ))}
                        </Section>
                    )}

                    {/* Interpretation */}
                    <InterpretationSection text={result.interpretation} />

                    {/* Sensitivity */}
                    <SensitivitySection data={result.analysis} />

                    {/* Debug */}
                    <RawJsonPanel data={result} />
                </>
            )}
        </main>
    );
}
