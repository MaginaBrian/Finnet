import { formatMoney, formatSignedMoney, formatSignedPercent } from "../utils/format";

describe("formatting", () => {
  it("prefixes the currency and groups thousands", () => {
    expect(formatMoney(1250000, "KES")).toBe("KES 1,250,000.00");
  });

  it("always shows a sign on profit and loss", () => {
    expect(formatSignedMoney(1500, "USD")).toBe("+USD 1,500.00");
    expect(formatSignedMoney(-1500, "USD")).toBe("\u2212USD 1,500.00");
    expect(formatSignedMoney(0, "USD")).toBe("USD 0.00");
  });

  it("formats percentages with signs", () => {
    expect(formatSignedPercent(12.345)).toBe("+12.35%");
    expect(formatSignedPercent(-3)).toBe("\u22123.00%");
  });
});
