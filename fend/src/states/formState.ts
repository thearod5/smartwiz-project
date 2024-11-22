import {create} from "zustand";

// Mock Feature to Load JSON Data into State

export interface TaxItem {
    id: string;
    type: "credit" | "deduction";
    name: string;
    amount: number;
    description: string;
    explanation: string;
    source: string;
}

export interface TaxState {
    salary: number;
    credits: TaxItem[];
    deductions: TaxItem[];
    addTaxItem: (item: TaxItem) => void;
    updateTaxItem: (id: string, updatedItem: Partial<TaxItem>) => void;
    setTaxItems: (items: TaxItem[]) => void;
    setSalary: (salary: number) => void;
}

const useFormState = create<TaxState>()((set) => ({
    salary: 0,
    credits: [],
    deductions: [],
    addTaxItem: (item) =>
        set((state) => {
            if (item.type === "credit") {
                return {credits: [...state.credits, item]};
            } else if (item.type === "deduction") {
                return {deductions: [...state.deductions, item]};
            }
            return state;
        }),
    updateTaxItem: (id, updatedItem) =>
        set((state) => ({
            credits: state.credits.map((item) =>
                item.id === id ? {...item, ...updatedItem} : item
            ),
            deductions: state.deductions.map((item) =>
                item.id === id ? {...item, ...updatedItem} : item
            ),
        })),
    setTaxItems: (items) =>
        set(() => ({
            credits: items.filter((item) => item.type === "credit"),
            deductions: items.filter((item) => item.type === "deduction"),
        })),
    setSalary: (salary) => set(() => ({salary})),
}));

export default useFormState;

