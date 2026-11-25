import { formatSignedMoney, formatSignedPercent, plClass } from "../utils/format";

export default function Pl({ value, currency, percent }) {
  return (
    <span className={`pl ${plClass(value)}`}>
      {formatSignedMoney(value, currency)}
      {percent !== undefined && ` (${formatSignedPercent(percent)})`}
    </span>
  );
}
