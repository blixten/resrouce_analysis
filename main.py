import streamlit as st
from openai import OpenAI
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import altair as alt
import pandas as pd

from utils import get_r_count, get_additional_rs_count, get_r_over_time, get_flow_counts, get_main_flow, get_categories

if 'OPENAI_API_KEY' in st.secrets:
    OpenAI.api_key = st.secrets["OPENAI_API_KEY"]

client = OpenAI()

if "data" not in st.session_state.keys():
    with open("combined_results.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    st.session_state["data"] = data

with st.sidebar:
    st.subheader("Re:Source")


tab_summary, tab_9R, tab_flows, tab_materials, tab_trl, tab_comm, tab_chat, tab_debug = st.tabs(["Övergripande", "9R Strategi", "Cirkulära flöden", "Material", "TRL", "Kommunikation", "Chat", "Debug"])

with tab_summary:

    st.write(st.session_state["data"]["results"]["summary"])
    wc_data = st.session_state["data"]["tags"]["wc_count"]
    wordcloud = WordCloud(background_color="white", width=1000, height=600).generate_from_frequencies(wc_data)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    st.pyplot(plt)

    categories = get_categories(st.session_state["data"])
    st.markdown(f"""Analysen berör för tillfället **{len(st.session_state["data"]["projects"])}** projekt och dess slutrapporter.
                Dessa projekt berör områden som {", ".join(list(categories)).lower()}. """)
    
    st.markdown("**Projektens övergripande syfte**")
    st.write("Projekten syftar till att främja cirkulär ekonomi och hållbar resursanvändning genom att utveckla och analysera tekniska, ekonomiska och organisatoriska lösningar inom återvinning, återanvändning och avfallsminimering. Flera projekt fokuserar på att identifiera aktörer, nätverk och institutioner för att stärka innovationssystemet och skapa policyunderlag. Andra mål är att utveckla nya metoder för rening och återvinning av material som plast, metaller, gips, fiberkompositer och elektronik, samt att optimera insamlings- och hanteringssystem för olika avfallsströmmar, såsom fritidsbåtar, matfett och plast på återvinningscentraler. Projekten adresserar även affärsmodeller, designförändringar och incitament för att öka återvinning och resurseffektivitet, särskilt inom bygg-, industri- och livsmedelssektorn. Vidare undersöks möjligheter till industriell symbios, kunskapsöverföring och samverkan mellan aktörer, samt utveckling av hållbarhetsbedömningar och livscykelanalyser för att identifiera miljömässigt och ekonomiskt hållbara lösningar. Genom dessa insatser vill projekten bidra till ökad återvinning, minskat matsvinn, förbättrad resursanvändning och en mer cirkulär och fossilfri ekonomi.")

    
with tab_9R:

    st.subheader("9R-Strategier")
    st.markdown("**Huvudsaklig 9R-strategi**")
    st.write("De 9R-strategierna är ett ramverk för cirkulär ekonomi som hjälper företag och samhällen att minska resursanvändning och avfall. De omfattar stegen Refuse, Rethink, Reduce, Reuse, Repair, Refurbish, Remanufacture, Repurpose och Recycle. Strategierna används för att prioritera åtgärder som förlänger produkters livslängd, ersätter engångsbruk med smartare lösningar och slutligen återvinner material när andra alternativ inte längre är möjliga. Tanken är att gå från linjära till cirkulära system där resurser hålls i kretslopp så länge som möjligt.")
    st.write("Analysen visar vilken strategi som är projektets huvudsakliga strategi")
    r_count = get_r_count(st.session_state["data"])
    st.bar_chart(r_count)


    st.markdown("**Övriga 9R-strategi**")
    st.write("Analysen visar antalet övriga strategier som projekten tillämpar, förutom den huvudsakliga strategin.")
    rs_counts = get_additional_rs_count(st.session_state["data"])
    st.bar_chart(rs_counts)
    st.write(st.session_state["data"]["nine_r"]["summary"])

    st.markdown("**R-Strategi över tid**")
    st.write("Analysen visar hur fokus kring de olika strategierna och dess implikationer har förändrats över tid.")
    r_over_time = st.session_state["data"]["nine_r"]["r_over_years"]
    st.line_chart(r_over_time)
    st.markdown("*Just nu visar grafen året då projektet startades, men det går lätt att ändra*")
    st.write(st.session_state["data"]["nine_r"]["r_over_time_summary"])

with tab_flows:
    st.subheader("Cirkulära flöden")
    st.write(st.session_state["data"]["flows"]["flows_summary"])
    st.markdown("**Identifierade strategier**")
    flows = st.session_state["data"]["flows"]["count"] #get_flow_counts(st.session_state["data"])
    st.bar_chart(flows)
    st.markdown("*Diagrammet visar det totala antalet identifierade flöden/cirkulära strategier*")

    st.markdown("**Primärt fokus bland cirkulära strategier**")
    main_flow = st.session_state["data"]["flows"]["main_flow"] #get_main_flow(st.session_state["data"])
    st.bar_chart(main_flow)
    st.markdown("*Diagrammet visar vad analysen identifierade som den huvudsakliga strategien i projekten*")
    st.write(st.session_state["data"]["flows"]["main_flow_summary"])

    st.markdown("**Fokus på strategi över åren**")
    st.markdown("*implementeras senare...*")

with tab_materials:
    st.subheader("Materiella resurser")

    st.bar_chart(st.session_state["data"]["materials"]["count"])
    st.write(st.session_state["data"]["materials"]["summary"])
    wc_data = st.session_state["data"]["materials"]["count"]
    wordcloud = WordCloud(background_color="white", width=1000, height=600).generate_from_frequencies(wc_data)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    st.pyplot(plt)

    

with tab_trl:
    st.subheader("TRL")
    st.bar_chart(st.session_state["data"]["trl"]["count"])

with tab_comm:
    st.subheader("Kommunikation")
    summaries = st.session_state["data"]["communication"]["summary"]

    
    internal_comm_categories = st.session_state["data"]["communication"]["internal_categories"]
    internal_freq = {}
    for cat in internal_comm_categories:
        internal_freq[cat] = internal_freq.get(cat, 0) + 1
    

    comm_count = {"0": 0, "1": 0, "2": 0,"3": 0,"4": 0,"5": 0,"6": 0,"7": 0,"8": 0,"9": 0,"10": 0,"11": 0,"12": 0,"13": 0,"15 eller mer": 0}
    for count in st.session_state["data"]["communication"]["count"]:
        if count >= 15:
            comm_count["15 eller mer"] += 1
        else:
            key = str(count)
            if key in comm_count:
                comm_count[key] += 1

    df = pd.DataFrame({
        "Antal kommunikationsinsatser": list(comm_count.keys()),
        "Antal projekt": list(comm_count.values())
    })
    
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("Antal kommunikationsinsatser", sort=list(comm_count.keys())),
        y="Antal projekt"
    )

    st.altair_chart(chart, use_container_width=True)   
    

    st.write(summaries[0])
    wordcloud = WordCloud(background_color="white", width=1000, height=600).generate_from_frequencies(internal_freq)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    st.pyplot(plt)



    external_comm_categories = st.session_state["data"]["communication"]["external_categories"]
    external_freq = {}
    for cat in external_comm_categories:
        external_freq[cat] = external_freq.get(cat, 0) + 1

    st.write(summaries[1])    
    wordcloud = WordCloud(background_color="white", width=1000, height=600).generate_from_frequencies(external_freq)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    st.pyplot(plt)


    st.write(summaries[2])

    planned_comm_categories = st.session_state["data"]["communication"]["planned_categories"]
    planned_freq = {}
    for cat in planned_comm_categories:
        planned_freq[cat] = planned_freq.get(cat, 0) + 1

    wordcloud = WordCloud(background_color="white", width=1000, height=600).generate_from_frequencies(planned_freq)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    st.pyplot(plt)




with tab_chat:
    st.subheader("Chat kommer snart...")

with tab_debug:
    stores = client.vector_stores.list()
    for store in stores:
        st.json(store, expanded=True)
