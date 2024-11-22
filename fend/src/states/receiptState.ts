import {create} from 'zustand';

interface ReceiptState {
    data: {
        attempt: string;
        id: string;
        request_id: string;
        status: string;
    } | null;
    setReceiptData: (data: ReceiptState['data']) => void;
    clearData: () => void;
}

const useReceiptStore = create<ReceiptState>((set) => ({
    data: null,
    setReceiptData: (data) => set({data}),
    clearData: () => set({data: null}),
}));

export default useReceiptStore;
