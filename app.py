import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="CareRewards Lead Manager",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Priority state tiers
TIER_1_STATES = ['MA', 'NY', 'CA']
TIER_2_STATES = ['IL', 'TX', 'PA', 'FL', 'NJ', 'OH']

@st.cache_data
def load_data():
    """Load and prepare the CRM data"""
    try:
        df = pd.read_csv('self_insured_crm_list.csv')
        
        # Add priority tier column
        df['Priority_Tier'] = df['State'].apply(
            lambda x: 'Tier 1' if x in TIER_1_STATES 
            else ('Tier 2' if x in TIER_2_STATES else 'Tier 3')
        )
        
        # Generate Perplexity query for each lead
        df['Perplexity_Query'] = df.apply(
            lambda row: f"Find the employee benefits decision-maker (HR Director, Benefits Manager, or CFO) for {row['Employer_Name']} (EIN: {row['EIN']}) in {row['State']}. Include their name, title, email, and phone if available.",
            axis=1
        )
        
        return df
    except FileNotFoundError:
        st.error("❌ Error: 'self_insured_crm_list.csv' not found. Please ensure the file is in the same directory as app.py")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.stop()

def create_summary_stats(df):
    """Create summary statistics visualizations"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Total Leads", f"{len(df):,}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Median Participants", f"{int(df['Participants'].median()):,}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        tier1_count = len(df[df['Priority_Tier'] == 'Tier 1'])
        st.metric("Tier 1 States", f"{tier1_count:,}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        large_market = len(df[df['Market_Segment'] == 'Large (5K+)'])
        st.metric("Large Market (5K+)", f"{large_market:,}")
        st.markdown('</div>', unsafe_allow_html=True)

def create_geographic_chart(df):
    """Create geographic distribution bar chart"""
    state_counts = df['State'].value_counts().head(15).reset_index()
    state_counts.columns = ['State', 'Count']
    
    # Add tier information
    state_counts['Tier'] = state_counts['State'].apply(
        lambda x: 'Tier 1' if x in TIER_1_STATES 
        else ('Tier 2' if x in TIER_2_STATES else 'Tier 3')
    )
    
    fig = px.bar(
        state_counts,
        x='State',
        y='Count',
        color='Tier',
        title='Top 15 States by Lead Count',
        color_discrete_map={'Tier 1': '#1f77b4', 'Tier 2': '#ff7f0e', 'Tier 3': '#2ca02c'}
    )
    fig.update_layout(height=400)
    return fig

def create_participant_distribution(df):
    """Create participant size distribution histogram"""
    fig = px.histogram(
        df,
        x='Participants',
        nbins=30,
        title='Distribution of Participants per Lead',
        labels={'Participants': 'Number of Participants', 'count': 'Number of Leads'}
    )
    fig.update_layout(height=400)
    return fig

def get_top_priority_leads(df, n=50):
    """Get top N priority leads based on tier and participant count"""
    # Sort by priority tier (Tier 1 first) then by participants descending
    tier_order = {'Tier 1': 0, 'Tier 2': 1, 'Tier 3': 2}
    df_sorted = df.copy()
    df_sorted['Tier_Rank'] = df_sorted['Priority_Tier'].map(tier_order)
    df_sorted = df_sorted.sort_values(['Tier_Rank', 'Participants'], ascending=[True, False])
    df_sorted = df_sorted.drop('Tier_Rank', axis=1)
    return df_sorted.head(n)

def main():
    # Header
    st.markdown('<div class="main-header">🏥 CareRewards Lead Manager</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Self-Insured Employer Pipeline | Market Segmentation & Prioritization</div>', unsafe_allow_html=True)
    
    # Load data
    df_original = load_data()
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Quick filter presets
    st.sidebar.subheader("Quick Filters")
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("Tier 1 States"):
            st.session_state.selected_states = TIER_1_STATES
            st.rerun()
    
    with col2:
        if st.button("All States"):
            st.session_state.selected_states = list(df_original['State'].dropna().unique())
            st.rerun()
    
    # Initialize session state for selected states if not exists
    if 'selected_states' not in st.session_state:
        st.session_state.selected_states = list(df_original['State'].dropna().unique())
    
    # State filter
    st.sidebar.subheader("Geographic Filters")
    all_states = sorted(df_original['State'].dropna().unique())
    selected_states = st.sidebar.multiselect(
        "Select States",
        options=all_states,
        default=st.session_state.selected_states,
        key='state_filter'
    )
    
    # Priority tier filter
    selected_tiers = st.sidebar.multiselect(
        "Priority Tiers",
        options=['Tier 1', 'Tier 2', 'Tier 3'],
        default=['Tier 1', 'Tier 2', 'Tier 3']
    )
    
    # Participant filters
    st.sidebar.subheader("Size Filters")
    
    # Quick participant buttons
    col1, col2, col3 = st.sidebar.columns(3)
    min_participants = 500
    
    with col1:
        if st.button("1K+"):
            min_participants = 1000
    with col2:
        if st.button("2.5K+"):
            min_participants = 2500
    with col3:
        if st.button("5K+"):
            min_participants = 5000
    
    # Participant slider
    participant_range = st.sidebar.slider(
        "Participants Range",
        min_value=int(df_original['Participants'].min()),
        max_value=int(df_original['Participants'].max()),
        value=(min_participants, int(df_original['Participants'].max())),
        step=100
    )
    
    # Market segment filter
    selected_segments = st.sidebar.multiselect(
        "Market Segment",
        options=df_original['Market_Segment'].unique(),
        default=df_original['Market_Segment'].unique()
    )
    
    # Search filters
    st.sidebar.subheader("Search")
    search_employer = st.sidebar.text_input("Employer Name")
    search_ein = st.sidebar.text_input("EIN")
    
    # Apply filters
    df_filtered = df_original.copy()
    
    if selected_states:
        df_filtered = df_filtered[df_filtered['State'].isin(selected_states)]
    
    if selected_tiers:
        df_filtered = df_filtered[df_filtered['Priority_Tier'].isin(selected_tiers)]
    
    df_filtered = df_filtered[
        (df_filtered['Participants'] >= participant_range[0]) &
        (df_filtered['Participants'] <= participant_range[1])
    ]
    
    if selected_segments:
        df_filtered = df_filtered[df_filtered['Market_Segment'].isin(selected_segments)]
    
    if search_employer:
        df_filtered = df_filtered[
            df_filtered['Employer_Name'].str.contains(search_employer, case=False, na=False)
        ]
    
    if search_ein:
        df_filtered = df_filtered[
            df_filtered['EIN'].astype(str).str.contains(search_ein, na=False)
        ]
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📋 Lead Table", "⭐ Top Priority"])
    
    with tab1:
        st.subheader("Summary Statistics")
        create_summary_stats(df_filtered)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if len(df_filtered) > 0:
                st.plotly_chart(create_geographic_chart(df_filtered), use_container_width=True)
            else:
                st.info("No data to display with current filters")
        
        with col2:
            if len(df_filtered) > 0:
                st.plotly_chart(create_participant_distribution(df_filtered), use_container_width=True)
            else:
                st.info("No data to display with current filters")
    
    with tab2:
        st.subheader(f"Filtered Leads ({len(df_filtered):,} results)")
        
        # Export buttons
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            csv_filtered = df_filtered.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Filtered Results",
                data=csv_filtered,
                file_name="careRewards_filtered_leads.csv",
                mime="text/csv",
                key='download_filtered'
            )
        
        with col2:
            # Export with Perplexity queries
            csv_with_queries = df_filtered[['Employer_Name', 'EIN', 'State', 'Participants', 
                                           'Market_Segment', 'Priority_Tier', 'Perplexity_Query']].to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download with Perplexity Queries",
                data=csv_with_queries,
                file_name="careRewards_leads_with_queries.csv",
                mime="text/csv",
                key='download_queries'
            )
        
        # Pagination
        leads_per_page = 50
        total_pages = (len(df_filtered) - 1) // leads_per_page + 1
        
        if total_pages > 0:
            page = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)
            start_idx = (page - 1) * leads_per_page
            end_idx = start_idx + leads_per_page
            
            # Display table
            display_cols = ['Employer_Name', 'EIN', 'State', 'Participants', 'Market_Segment', 'Priority_Tier', 'Plan_Name']
            df_page = df_filtered[display_cols].iloc[start_idx:end_idx]
            
            st.dataframe(
                df_page,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Employer_Name": st.column_config.TextColumn("Employer", width="medium"),
                    "EIN": st.column_config.NumberColumn("EIN", format="%d"),
                    "State": st.column_config.TextColumn("State", width="small"),
                    "Participants": st.column_config.NumberColumn("Participants", format="%d"),
                    "Market_Segment": st.column_config.TextColumn("Segment", width="small"),
                    "Priority_Tier": st.column_config.TextColumn("Tier", width="small"),
                    "Plan_Name": st.column_config.TextColumn("Plan Name", width="large")
                }
            )
            
            st.caption(f"Showing {start_idx + 1}-{min(end_idx, len(df_filtered))} of {len(df_filtered):,} leads")
            
            # Individual Perplexity query generator
            st.markdown("---")
            st.subheader("🔍 Generate Perplexity Query for Individual Lead")
            
            selected_employer = st.selectbox(
                "Select Employer",
                options=df_page['Employer_Name'].tolist(),
                key='perplexity_employer'
            )
            
            if selected_employer:
                lead_data = df_filtered[df_filtered['Employer_Name'] == selected_employer].iloc[0]
                query = lead_data['Perplexity_Query']
                
                st.text_area(
                    "Copy this query to Perplexity Pro:",
                    value=query,
                    height=100,
                    key='query_display'
                )
                
                st.info("💡 Tip: Copy the query above, paste into Perplexity Pro, and save the contact details separately (v2 will include in-app storage)")
        else:
            st.info("No leads match your current filters")
    
    with tab3:
        st.subheader("⭐ Top 50 Priority Leads")
        st.markdown("*Sorted by: Tier 1 states first, then by participant count (descending)*")
        
        top_leads = get_top_priority_leads(df_filtered, n=50)
        
        # Quick export button
        csv_top50 = top_leads[['Employer_Name', 'EIN', 'State', 'Participants', 
                               'Market_Segment', 'Priority_Tier', 'Perplexity_Query']].to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="📥 Export Top 50 Priority Leads (Instant Outreach CSV)",
            data=csv_top50,
            file_name="careRewards_top50_priority.csv",
            mime="text/csv",
            key='download_top50',
            type="primary"
        )
        
        st.markdown("---")
        
        # Display top 50 table
        display_cols = ['Employer_Name', 'EIN', 'State', 'Participants', 'Market_Segment', 'Priority_Tier']
        
        st.dataframe(
            top_leads[display_cols],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Employer_Name": st.column_config.TextColumn("Employer", width="medium"),
                "EIN": st.column_config.NumberColumn("EIN", format="%d"),
                "State": st.column_config.TextColumn("State", width="small"),
                "Participants": st.column_config.NumberColumn("Participants", format="%d"),
                "Market_Segment": st.column_config.TextColumn("Segment", width="small"),
                "Priority_Tier": st.column_config.TextColumn("Tier", width="small")
            }
        )
        
        # Priority breakdown
        st.markdown("---")
        st.subheader("Priority Breakdown")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            tier1_count = len(top_leads[top_leads['Priority_Tier'] == 'Tier 1'])
            st.metric("Tier 1 Leads", tier1_count)
        
        with col2:
            avg_participants = int(top_leads['Participants'].mean())
            st.metric("Avg Participants", f"{avg_participants:,}")
        
        with col3:
            large_count = len(top_leads[top_leads['Market_Segment'] == 'Large (5K+)'])
            st.metric("Large Market", large_count)

if __name__ == "__main__":
    main()
