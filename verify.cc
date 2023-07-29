#include <iostream>
#include <fstream>
{
    ofstream myfile,myfile1,myfile2;
    myfile.open ("angle_4000.txt");
    myfile1.open ("Map_4000.txt");
    myfile2.open ("Energy_4000.txt");
    TFile *fin1 = new TFile("gamma50_150_4000MeV_uniformTheta_uniformPhi_n300K_overlap_skims.root");
    TTree *pi0Tree = (TTree*)fin1->Get("pi0Tree");

    TFile *fin2 = new TFile("gamma50_150_4000MeV_uniformTheta_uniformPhi_n300K_overlap_skims_CR.root");
    TTree *pi0CRTree = (TTree*)fin2->Get("pi0CRTree");

    int event_t;
    double gamma0E_t, gamma0MCE_t;
    double gamma1E_t, gamma1MCE_t;
    double E,M,dAngle;
    double gamma0Theta, gamma0MCTheta, gamma0Phi, gamma0MCPhi, gamma1Theta, gamma1MCTheta, gamma1Phi, gamma1MCPhi;

    pi0Tree->SetBranchAddress("__event__",&event_t);
    pi0Tree->SetBranchAddress("E",&E);
    pi0Tree->SetBranchAddress("gamma0E",&gamma0E_t);
    pi0Tree->SetBranchAddress("gamma0MCE",&gamma0MCE_t);
    pi0Tree->SetBranchAddress("gamma1E",&gamma1E_t);
    pi0Tree->SetBranchAddress("gamma1MCE",&gamma1MCE_t);

    pi0Tree->SetBranchAddress("M",&M);
    pi0Tree->SetBranchAddress("dAngle",&dAngle);
    
    pi0Tree->SetBranchAddress("gamma0Theta",&gamma0Theta);
    pi0Tree->SetBranchAddress("gamma0MCTheta",&gamma0MCTheta);
    pi0Tree->SetBranchAddress("gamma0Phi",&gamma0Phi);
    pi0Tree->SetBranchAddress("gamma0MCPhi",&gamma0MCPhi);
    pi0Tree->SetBranchAddress("gamma1Theta",&gamma1Theta);
    pi0Tree->SetBranchAddress("gamma1MCTheta",&gamma1MCTheta);
    pi0Tree->SetBranchAddress("gamma1Phi",&gamma1Phi);
    pi0Tree->SetBranchAddress("gamma1MCPhi",&gamma1MCPhi);

    int CRevent_t;
    double CRCellEMap_t[27][50];
    pi0CRTree->SetBranchAddress("__event__",&CRevent_t);
    pi0CRTree->SetBranchAddress("CRCellEMap",&CRCellEMap_t);


    for(int evt=0;evt<1142696;++evt) {
      pi0Tree->GetEntry(evt);
      pi0CRTree->GetEntry(evt);

      cout << "entry = " << evt << endl;
      cout << "event pi0,pi0CR = " << event_t << ", " << CRevent_t << endl;
      cout << "gamma0 E, MCE = " << gamma0E_t << ", " << gamma0MCE_t << endl;
      cout << "gamma1 E, MCE = " << gamma1E_t << ", " << gamma1MCE_t << endl;
      
      myfile << M<< ' '<< dAngle<< ' '<< gamma0Theta<< ' '<< gamma0MCTheta<< ' '<< gamma0Phi<< ' '<< gamma0MCPhi<< ' '<< gamma1Theta<< ' '<< gamma1MCTheta<< ' '<< gamma1Phi<< ' '<< gamma1MCPhi<< ' '; 
      myfile2 << E<<  ' '<< gamma0E_t<< ' '<< gamma0MCE_t<< ' '<< gamma1E_t<< ' '<< gamma1MCE_t<< ' '<<evt<<' '<< event_t << " " << CRevent_t <<" "; 

      cout << "gamma0MCTheta, gamma0MCPhi = " << gamma0MCTheta << ", " << gamma0MCPhi << endl;
      cout << "gamma1MCTheta, gamma1MCPhi = " << gamma1MCTheta << ", " << gamma1MCPhi << endl;
     
      double E_sum = 0.;
      for(int i=0;i<50;++i)
        for(int j=0;j<27;++j) E_sum += CRCellEMap_t[j][i];
      cout << "E_sum = " << E_sum << endl;
      cout << "E_sum/(g0E+g1E) = " << E_sum/(gamma0E_t+gamma1E_t) << endl;
      cout << "E_sum/(g0MCE+g1MCE) = " << E_sum/(gamma0MCE_t+gamma1MCE_t) << endl;

      for(int i=0;i<50;++i) {
        for(int j=0;j<27;++j) {
          if (CRCellEMap_t[j][i]!=0) myfile1 << "("<<j <<","<<i<<","<<CRCellEMap_t[j][i]<<")"<< ' ';
          //if (CRCellEMap_t[j][i]>1E-5) printf("\033[0;31m%.3f\033[0m ",CRCellEMap_t[j][i]);
          //else printf("%.3f ",CRCellEMap_t[j][i]);
        }
        //printf("\n");
       
      }

      cout << endl;
      myfile<<'\n';
      myfile1<<'\n';
      myfile2<<'\n';

    }
    myfile.close(); 
    myfile1.close(); 
    myfile2.close(); 

}
