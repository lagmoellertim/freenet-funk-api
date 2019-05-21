getDataSchema = """
query CustomerForDashboardQuery {
  me {
    ...CustomerForDashboardFragment
    __typename
  }
}

fragment CustomerForDashboardFragment on Customer {
  id
  details {
    ...DetailsFragment
    __typename
  }
  customerProducts {
    ...ProductFragment
    __typename
  }
  __typename
}

fragment DetailsFragment on Details {
  firstName
  lastName
  dateOfBirth
  contactEmail
  __typename
}

fragment ProductFragment on FUNKCustomerProduct {
  id
  state
  paymentMethods {
    ...PaymentMethodFragment
    __typename
  }
  mobileNumbers {
    ...MobileNumberFragment
    __typename
  }
  sims {
    ...SIMFragment
    __typename
  }
  tariffs: tariffCustomerProductServices {
    ...TariffFragment
    __typename
  }
  __typename
}

fragment PaymentMethodFragment on PaymentMethod {
  id
  state
  approvalChallenge {
    approvalURL
    __typename
  }
  agreement {
    state
    payerInfo {
      payerID
      email
      __typename
    }
    __typename
  }
  __typename
}

fragment MobileNumberFragment on MobileNumberCPS {
  id
  number
  state
  usage {
    usedDataPercentage
    __typename
  }
  productServiceId
  productServiceInfo {
    id
    label
    __typename
  }
  ... on MNPImportCustomerProductService {
    otherProviderShortcut
    otherProviderCustomName
    otherContract {
      contractType
      mobileNumber
      mobileNumberIsVerified
      __typename
    }
    mnpInfos {
      confirmedPortingDate
      lastPortingResult
      problemCode
      problemReason
      __typename
    }
    __typename
  }
  __typename
}

fragment SIMFragment on SIMCustomerProductService {
  id
  networkState
  state
  iccid
  delivery {
    state
    trackingDetails {
      stateId
      stateLabel
      trackingURL
      __typename
    }
    deliveryProvider
    address {
      city
      additionalInfo
      __typename
    }
    __typename
  }
  __typename
}

fragment TariffFragment on TariffCustomerProductService {
  id
  booked
  starts
  state
  productServiceId
  productServiceInfo {
    id
    label
    follower {
      id
      label
      __typename
    }
    marketingInfo {
      name
      __typename
    }
    __typename
  }
  __typename
}
"""

orderPlanSchema = """
mutation AddTariffToProductMutation($productID: String!, $tariffID: String!) {
  tariffAddToCustomerProduct(customerProductId: $productID, productServiceId: $tariffID) {
    ...TariffFragment
    __typename
  }
}

fragment TariffFragment on TariffCustomerProductService {
  id
  booked
  starts
  state
  productServiceId
  productServiceInfo {
    id
    label
    follower {
      id
      label
      __typename
    }
    marketingInfo {
      name
      __typename
    }
    __typename
  }
  __typename
}
"""

removeProductSchema = """
mutation TerminateTariffMutation($tariffID: String!) {
  tariffTerminate(customerProductServiceId: $tariffID) {
    TariffFragment
    __typename
  }
}

fragment TariffFragment on TariffCustomerProductService {
  id
  booked
  starts
  state
  productServiceId
  productServiceInfo {
    id
    label
    follower {
      id
      label
      __typename
    }
    marketingInfo {
      name
      __typename
    }
    __typename
  }
  __typename
}
"""