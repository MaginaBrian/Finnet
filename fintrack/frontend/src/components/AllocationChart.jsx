import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
import { useColorScheme } from "../hooks/useColorScheme";
import { formatMoney, formatPercent } from "../utils/format";
import { EmptyState } from "./StateViews";

/** Reads the palette from the CSS tokens so the chart follows the brand and dark mode. */
function readTokens() {
  const css = getComputedStyle(document.documentElement);
  return {
    palette: [1, 2, 3, 4, 5, 6].map((i) => css.getPropertyValue(`--chart-${i}`).trim() || "#0b1f3a"),
    surface: css.getPropertyValue("--surface").trim() || "#ffffff",
  };
}

export default function AllocationChart({ holdings, currency, totalValue }) {
  const scheme = useColorScheme();
  const { palette, surface } = readTokens(scheme);

  if (holdings.length === 0) {
    return <EmptyState title="Nothing to chart yet">The allocation chart shows once the portfolio holds something.</EmptyState>;
  }

  const data = holdings.map((h) => ({ name: h.instrument, value: h.total_value, pct: h.allocation_pct }));
  const colour = (i) => palette[i % palette.length];

  return (
    <div className="chart">
      <div className="chart__plot" role="img" aria-label={`Allocation by value: ${data.map((d) => `${d.name} ${formatPercent(d.pct)}`).join(", ")}`}>
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie data={data} dataKey="value" nameKey="name" innerRadius="62%" outerRadius="92%" paddingAngle={2} stroke={surface} isAnimationActive={false}>
              {data.map((d, i) => (
                <Cell key={d.name} fill={colour(i)} />
              ))}
            </Pie>
            <Tooltip formatter={(v) => formatMoney(v, currency)} />
          </PieChart>
        </ResponsiveContainer>
        <div className="chart__center">
          <span>Total value</span>
          <strong>{formatMoney(totalValue, currency)}</strong>
        </div>
      </div>
      <ul className="legend">
        {data.map((d, i) => (
          <li key={d.name}>
            <span className="legend__swatch" style={{ background: colour(i) }} aria-hidden="true" />
            <span>{d.name}</span>
            <span className="legend__pct">{formatPercent(d.pct)}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
